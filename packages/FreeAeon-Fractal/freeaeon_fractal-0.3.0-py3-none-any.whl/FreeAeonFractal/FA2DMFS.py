'''
Basic operations for 2D shapes
1. Calculation of multifractal spectra
'''
import matplotlib.pyplot as plt
import numpy as np
import cv2,math,json,os,sys
from tqdm import tqdm
from scipy.stats import linregress
import pandas as pd
from FreeAeonFractal.FAImage import CFAImage
import seaborn as sns
import matplotlib.ticker as mticker
from scipy.interpolate import UnivariateSpline

'''
Calculation of multifractal spectrum for 2D shapes
'''
class CFA2DMFS:
    '''
    image: input image (single channel)
    q_list: range of q values
    corp_type: image cropping method (-1: crop, 0: no processing, 1: padding)
    '''
    def __init__(self, image, corp_type = -1, q_list=np.linspace(-5, 5, 51) , with_progress= True ):
        tmp_img = image.astype(np.float64)
        tmp_img -= np.min(tmp_img)
        tmp_img /= (np.max(tmp_img) + 1e-12)
        self.m_image = tmp_img / np.max(tmp_img)  # normalize image

        self.m_corp_type = corp_type  # image cropping mode: -1 crop, 0 no processing, 1 padding
        self.m_q_list = []
        # avoid q == 1 case (ignored)
        for q in q_list:
           if q == 1:
               self.m_q_list.append( q )
               #self.m_q_list.append( q - np.finfo(float).eps )
           else:
               self.m_q_list.append( q )
        self.m_with_progress = with_progress

    '''Get generalized mass distribution
    max_size: max box size for partitioning
    Returns: generalized mass distribution
    '''
    def get_mass(self, max_size=None, max_scales=200):
        all_data = []

        if max_size is None:
            max_size = min(self.m_image.shape)  
        if max_size < 4:
            raise ValueError("max_size too small: must be >= 4")

        # get box size ( ε ) list
        scales = np.logspace(1, np.log2(max_size), num=max_scales, base=2, dtype=int)
        scales = np.unique(scales)

        q_list = self.m_q_list
        image = self.m_image.astype(np.float64)  # for large numbers
        progress_iter = tqdm(scales, desc="Calculating mass") if self.m_with_progress else scales

        for size in progress_iter:
            if size < 4:
                continue
            block_size = (size, size)
            boxes, raw_blocks = CFAImage.get_boxes_from_image(image, block_size, corp_type=self.m_corp_type)
            no_zero_box = [box for box in boxes if np.count_nonzero(box) > 0]
            if len(no_zero_box) == 0:
                continue

            # Step 1: Calculate boxes mass
            mass_distribution = np.array([np.sum(box) for box in boxes], dtype=np.float64)
            mass_distribution = np.where(mass_distribution < 0, 0, mass_distribution)

            total_mass = np.sum(mass_distribution)
            if total_mass <= 0 or np.isnan(total_mass) or np.isinf(total_mass):
                continue

            mass_distribution /= total_mass
            mass_distribution = np.clip(mass_distribution, 1e-12, 1.0) # Prevent zero or extreme values

            # Step 2: Calculate M(q, ε)
            for q in q_list:
                tmp = {'scale': size, 'q': q, 'boxes': raw_blocks}

                if np.all(mass_distribution == 0):
                    tmp['mass'] = 0
                    all_data.append(tmp)
                    continue

                if q == 0:
                    tmp['mass'] = np.count_nonzero(mass_distribution)
                else:
                    # Numerically stable computation: mass^q = exp(q * log(mass))
                    log_mass = np.log(mass_distribution)
                    q_log_mass = q * log_mass

                    # Limit extreme values to prevent exp overflow
                    q_log_mass = np.clip(q_log_mass, a_min=-700, a_max=700)
                    mass_q = np.sum(np.exp(q_log_mass))

                    if np.isnan(mass_q) or np.isinf(mass_q):
                        mass_q = 0
                    tmp['mass'] = mass_q

                all_data.append(tmp)

        df = pd.DataFrame(all_data)
        return df.sort_values(by=['q', 'scale']).reset_index(drop=True)
    
    '''Calculate scaling exponent tau
    df_mass: generalized mass distribution dataframe
    Returns: q list and scaling exponent (tau) list
    '''
    def get_tau_q(self,df_mass):
        all_data = []
        if self.m_with_progress:
            for q, df_q in tqdm(df_mass.groupby("q"),desc="Calculating τ(q)"):
                tmp = {}
                if q == 1:
                    #mass = np.array(df_q['mass'].tolist())
                    #mass = mass[mass>0]
                    #tau = -np.sum(mass * np.log(mass))
                    #tmp['q'] = q
                    #tmp['t(q)'] = tau
                    entropy_list = []
                    log_scales = []
                    for scale, df_scale in df_q.groupby('scale'):
                        mass = np.array(df_scale['mass'])
                        mass = mass[mass > 0]
                        entropy = -np.sum(mass * np.log(mass))
                        entropy_list.append(entropy)
                        log_scales.append(np.log(scale))
                    if len(log_scales) > 5:
                        slope, intercept, r_value, p_value, std_err = linregress(log_scales, entropy_list)
                        tau = slope
                        tmp['q'] = q
                        tmp['t(q)'] = slope
                        tmp['intercept'] = intercept
                        tmp['r_value'] = r_value
                        tmp['p_value'] = p_value
                        tmp['std_err'] = std_err
                    else:
                        tau = np.nan
                        tmp['q'] = q
                        tmp['t(q)'] = tau
                else:
                    log_scales = np.log(df_q['scale'])
                    log_mass = np.log(df_q['mass'])
                    log_mass = np.where(log_mass == -np.inf, np.nan, log_mass)
                    valid_mask = np.isfinite(log_mass)
                    log_mass_valid = log_mass[valid_mask]
                    log_scales_valid = log_scales[valid_mask]
                    if len(log_scales_valid) > 5:
                        slope, intercept, r_value, p_value, std_err = linregress(log_scales_valid, log_mass_valid)
                        #slope, _ = np.polyfit(log_scales_valid, log_mass_valid, 1)
                        tmp['q'] = q
                        tmp['t(q)'] = slope
                        tmp['intercept'] = intercept
                        tmp['r_value'] = r_value
                        tmp['p_value'] = p_value
                        tmp['std_err'] = std_err
                    else:
                        tmp['q'] = q
                        tmp['t(q)'] = np.nan
                all_data.append(tmp)
        else:
            for q, df_q in df_mass.groupby("q"):
                tmp = {}
                if q == 1:
                    mass = np.array(df_q['mass'].tolist())
                    mass = mass[mass>0]
                    tau = -np.sum(mass * np.log(mass))
                    tmp['q'] = q
                    tmp['t(q)'] = tau
                else:
                    log_scales = np.log(df_q['scale'])
                    log_mass = np.log(df_q['mass'])
                    log_mass = np.where(log_mass == -np.inf, np.nan, log_mass)
                    valid_mask = np.isfinite(log_mass)
                    log_mass_valid = log_mass[valid_mask]
                    log_scales_valid = log_scales[valid_mask]
                    if len(log_scales_valid) > 5:
                        slope, intercept, r_value, p_value, std_err = linregress(log_scales_valid, log_mass_valid)
                        #slope, _ = np.polyfit(log_scales_valid, log_mass_valid, 1)
                        tmp['q'] = q
                        tmp['t(q)'] = slope
                        tmp['intercept'] = intercept
                        tmp['r_value'] = r_value
                        tmp['p_value'] = p_value
                        tmp['std_err'] = std_err
                    else:
                        tmp['q'] = q
                        tmp['t(q)'] = np.nan
                all_data.append(tmp)
        return pd.DataFrame(all_data)

    '''Calculate the generalized fractal dimension
    item: a single record in tau (value corresponding to a certain q)
    Returns: generalized fractal dimension (D)
    '''
    def get_generalized_dimension(self,df_tau):
        df_tau = self.get_alpha_f_alpha(df_tau)
        def calc_dimension(item):
            if item['q'] == 1:
                return item['a(q)']  # 用 alpha(1) 作为 d(1)
            else:
                return item['t(q)'] / (item['q'] - 1)
        df_tau['d(q)'] = df_tau.apply(calc_dimension, axis=1)
        return df_tau
        #def calc_dimension(item):
        #    if item['q'] == 1:
        #        return item['t(q)']  # use tau(q) when q is 1
        #    else:
        #        return item['t(q)'] / (item['q'] - 1)
        #df_tau['d(q)'] = df_tau.progress_apply(calc_dimension, axis=1)
        #df_tau['d(q)'] = df_tau.apply(calc_dimension, axis=1)
        #return df_tau

    '''Calculate the local singularity exponent and singularity spectrum
    df_tau: scaling data DataFrame df_tau
    Returns: list of local singularity exponents (alpha) and singularity spectrum (f(alpha))
    '''
    def get_alpha_f_alpha(self,df_tau):
        #alpha_list = np.gradient(df_tau['t(q)'], df_tau['q'])
        #f_alpha_list = df_tau['q'] * alpha_list - df_tau['t(q)']
        q_vals = df_tau['q'].values
        tq_vals = df_tau['t(q)'].values
        spl = UnivariateSpline(q_vals, tq_vals, k=3, s=0)
        alpha_list = spl.derivative()(q_vals)
        f_alpha_list = q_vals * alpha_list - tq_vals

        df_tau['a(q)'] = alpha_list
        df_tau['f(a)'] = f_alpha_list
        return df_tau
    
    '''Calculate multifractal spectrum from tau(q)
    df_tau: dataframe of tau(q)
    Returns: dataframe with q, alpha, f(alpha)
    '''
    def get_mfs(self, max_size = None, max_scales = 100 ):
        df_mass = self.get_mass(max_size = max_size, max_scales = max_scales )
        df_mfs = self.get_tau_q(df_mass)
        df_mfs = self.get_generalized_dimension(df_mfs)
        df_mfs = self.get_alpha_f_alpha(df_mfs)
        return df_mass,df_mfs
    
    '''Plot multifractal spectrum'''
    def plot(self, df_mass,df_mfs):
        fig, axs = plt.subplots(2, 3, figsize=(16, 8))
        
        #  mass vs scale vs. q
        vmin = np.percentile(df_mass['mass'], 25)   #  5% percentage
        vmax = np.percentile(df_mass['mass'], 75)  #  95% percentage
        df_pivot = df_mass.pivot(index='scale', columns='q', values='mass')
        sns.heatmap(df_pivot,ax=axs[0, 0], cmap='coolwarm',vmin=vmin, vmax=vmax, annot=False, cbar=True)
        axs[0, 0].set(xlabel=r'$scale$', ylabel=r'$q$', title=r'mass vs. scale vs. q')
        axs[0, 0].xaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
        axs[0, 0].set_xticklabels(axs[0, 0].get_xticklabels(), rotation=60)
        axs[0, 0].grid(True)

        #  tau(q) vs. q
        df_tmp = df_mfs.groupby("q").mean().reset_index().sort_values(by = "q").reset_index()
        sns.lineplot(data=df_tmp, x='q', y='t(q)', ax=axs[0, 1])
        axs[0, 1].set(xlabel='$q$', ylabel=r'$\tau(q)$', title=r'$\tau(q)$ vs. $q$')
        axs[0, 1].grid(True)

        #  D(q) vs. q
        df_tmp = df_mfs.groupby("q").mean().reset_index().sort_values(by = "q").reset_index()
        sns.lineplot(data=df_tmp, x='q', y='d(q)', ax=axs[0, 2])
        axs[0, 2].set(xlabel='$q$', ylabel=r'$D(q)$', title=r'$D(q)$ vs. $q$')
        axs[0, 2].grid(True)

        #  α(q) vs. q
        df_tmp = df_mfs.groupby("q").mean().reset_index().sort_values(by = "q").reset_index()
        sns.lineplot(data=df_tmp, x='q', y='a(q)', ax=axs[1, 0])
        axs[1, 0].set(xlabel='$q$', ylabel=r'$\alpha$', title=r'$\alpha(q)$ vs. $q$')
        axs[1, 0].grid(True)

        #  f(α) vs. α
        df_tmp = df_mfs.groupby("a(q)").mean().reset_index().sort_values(by = "a(q)").reset_index()
        sns.lineplot(data=df_tmp, x='a(q)', y='f(a)', ax=axs[1, 1])
        axs[1, 1].set(xlabel=r'$\alpha$', ylabel=r'f$(\alpha)$', title=r'$f(\alpha)$ vs. $\alpha$')
        axs[1, 1].grid(True)

        #  f(α) vs. d
        df_tmp = df_mfs.groupby("q").mean().reset_index().sort_values(by = "q").reset_index()
        df_tmp['tmp'] = (df_tmp['t(q)'] - df_tmp['t(q)'].min()) / (df_tmp['t(q)'].std())
        sns.lineplot(data=df_tmp, x='q', y='tmp', ax=axs[1, 2],label=r'$t(q)$')

        df_tmp['tmp'] = (df_tmp['d(q)'] - df_tmp['d(q)'].min()) / (df_tmp['d(q)'].std())
        sns.lineplot(data=df_tmp, x='q', y='tmp', ax=axs[1, 2],label=r'$d(q)$')

        df_tmp['tmp'] = (df_tmp['a(q)'] - df_tmp['a(q)'].min()) / (df_tmp['a(q)'].std())
        sns.lineplot(data=df_tmp, x='q', y='tmp', ax=axs[1, 2],label=r'$a(q)$')

        df_tmp['tmp'] = (df_tmp['f(a)'] - df_tmp['f(a)'].min()) / (df_tmp['f(a)'].std())
        sns.lineplot(data=df_tmp, x='q', y='tmp', ax=axs[1, 2],label=r'$f(a)$')

        axs[1, 2].set(xlabel=r'$q$', ylabel=r'$mix$', title=r'$overview$ vs. $q$')
        axs[1, 2].grid(True)
        
        plt.tight_layout()
        plt.show()

def main():
    image = cv2.imread("../images/fractal.png", cv2.IMREAD_GRAYSCALE)
    MFS = CFA2DMFS(image)
    df_mass,df_mfs = MFS.get_mfs()
    MFS.plot(df_mass,df_mfs)


if __name__ == "__main__":
    main()
