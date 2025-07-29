import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Import DebiasedLasso from econml
from econml.sklearn_extensions.linear_model import DebiasedLasso

class HTELasso:
    """
    Implementation of the proposed approach for detecting treatment effect heterogeneity:
    1. Transform outcome: y* = y * (t - p) / (p * (1 - p))
    2. Run debiased lasso on y* ~ X to identify significant moderators
    """
    
    def __init__(self, alpha=None, random_state=42, fit_intercept=True):
        """
        Initialize the detector
        
        Parameters:
        -----------
        alpha : float, optional
            Regularization parameter for Lasso. If None, will be selected via CV
        random_state : int
            Random seed for reproducibility
        fit_intercept : bool
            Whether to fit an intercept term
        """
        self.alpha = alpha
        self.random_state = random_state
        self.fit_intercept = fit_intercept
        
        self.scaler = StandardScaler()
        self.debiased_lasso = None
        self.y_star = None
        self.significant_vars = None
        self.coefficients = None
        self.std_errors = None
        self.confidence_intervals = None
        self.p_values = None
        
    def transform_outcome(self, y, t):
        """
        Transform the outcome variable according to: y* = y * (t - p) / (p * (1 - p))
        where p is calculated as the mean of t
        
        Parameters:
        -----------
        y : array-like
            Outcome variable
        t : array-like
            Treatment indicator (0 or 1)
            
        Returns:
        --------
        y_star : array-like
            Transformed outcome variable
        """
        y = np.array(y)
        t = np.array(t)
        
        # Calculate p as the mean of t
        p = np.mean(t)
            
        # Check for valid probability values
        if p <= 0 or p >= 1:
            raise ValueError("Treatment probability p must be between 0 and 1")
            
        # Compute transformation
        denominator = p * (1 - p)
        y_star = y * (t - p) / denominator
        
        return y_star
    
    def fit(self, X, y, t):
        """
        Fit the debiased lasso model to detect heterogeneity
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Covariate matrix
        y : array-like, shape (n_samples,)
            Outcome variable
        t : array-like, shape (n_samples,)
            Treatment indicator
            
        Returns:
        --------
        self : object
            Returns self for method chaining
        """
        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)
        t = np.array(t)
        
        # Transform outcome
        self.y_star = self.transform_outcome(y, t)
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Use DebiasedLasso from econml
        self.debiased_lasso = DebiasedLasso(
            alpha='auto',
            random_state=self.random_state,
            fit_intercept=self.fit_intercept
        )
        
        # Fit the model
        self.debiased_lasso.fit(X_scaled, self.y_star)
        
        # Extract results
        self.coefficients = self.debiased_lasso.coef_
        self.std_errors = self.debiased_lasso.coef_stderr_
        ci_alpha = 0.05 if self.alpha is None else self.alpha
        ci_lower, ci_upper = self.debiased_lasso.coef__interval(alpha=ci_alpha)
        self.confidence_intervals = np.column_stack([ci_lower, ci_upper])
        
        # Calculate p-values using t-statistics
        t_stats = self.coefficients / (self.std_errors + 1e-8)  # Add small epsilon for numerical stability
        self.p_values = 2 * (1 - stats.norm.cdf(np.abs(t_stats)))
        
        # Identify significant variables
        self.significant_vars = np.where(self.p_values < 0.05)[0]
        
        return self
    
    def predict_heterogeneity(self, X):
        """
        Predict heterogeneity scores for new data
        
        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Covariate matrix
            
        Returns:
        --------
        het_scores : array-like
            Predicted heterogeneity scores
        """
        if self.debiased_lasso is None:
            raise ValueError("Model not fitted yet. Call fit() first.")
            
        X_scaled = self.scaler.transform(X)
        return self.debiased_lasso.predict(X_scaled)
    
    def summary(self, feature_names=None, alpha=None):
        """
        Generate a statsmodels-like regression summary
        
        Parameters:
        -----------
        feature_names : list, optional
            Names of features
        alpha : float, optional
            Significance level
            
        Returns:
        --------
        summary_str : str
            Formatted regression summary similar to statsmodels
        """
        if self.coefficients is None:
            raise ValueError("Model not fitted yet. Call fit() first.")
            
        if alpha is None:
            alpha = 0.05 if self.alpha is None else self.alpha
            
        if feature_names is None:
            feature_names = [f"X{i}" for i in range(len(self.coefficients))]
        
        # Calculate t-statistics
        t_stats = self.coefficients / (self.std_errors + 1e-8)
        
        # Find active variables (non-zero coefficients)
        active_mask = np.abs(self.coefficients) > 1e-8
        active_indices = np.where(active_mask)[0]
        
        # Format the output
        output = []
        output.append("=" * 80)
        output.append("Treatment Effect Heterogeneity Detection Results")
        output.append("=" * 80)
        output.append("")
        
        # Model info
        output.append(f"Number of Observations: {len(self.y_star)}")
        output.append(f"Total Number of Features: {len(self.coefficients)}")
        output.append(f"Number of Active Variables: {len(active_indices)}")
        output.append(f"Number of Significant Moderators: {np.sum(self.p_values < alpha)}")
        alpha_value = self.debiased_lasso.selected_alpha_ if self.debiased_lasso.selected_alpha_ is not None else self.debiased_lasso.alpha
        output.append(f"Tuning Parameter alpha: {alpha_value:.3f}")
        output.append("")

        # Coefficients table (only active variables)
        output.append("Coefficients (Active Variables Only):")
        output.append("-" * 80)
        output.append(f"{'Feature':<15} {'Coef.':<12} {'Std.Err.':<12} {'t':<10} {'P>|t|':<10} {'[0.025':<8} {'0.975]':<8}")
        output.append("-" * 80)
        
        for idx in active_indices:
            feature = feature_names[idx]
            coef = self.coefficients[idx]
            std_err = self.std_errors[idx]
            p_val = self.p_values[idx]
            ci_lower = self.confidence_intervals[idx, 0]
            ci_upper = self.confidence_intervals[idx, 1]
            t_stat = t_stats[idx]
            
            # Format p-value
            if p_val < 0.001:
                p_str = "0.000"
            else:
                p_str = f"{p_val:.3f}"
            
            # Add significance stars
            if p_val < 0.001:
                sig = "***"
            elif p_val < 0.01:
                sig = "**"
            elif p_val < 0.05:
                sig = "*"
            else:
                sig = ""
            
            output.append(f"{feature:<15} {coef:>11.4f} {std_err:>11.4f} {t_stat:>9.3f} {p_str:>9} {ci_lower:>7.3f} {ci_upper:>7.3f}{sig}")
        
        output.append("-" * 80)
        output.append("Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1")
        output.append("")
        
        # Additional notes
        output.append("Additional Notes:")
        output.append("-" * 80)
        output.append("1. Outcome transformation: Y* = Y * (T - p) / (p * (1 - p))")
        output.append("2. Debiased Lasso regression on Y* ~ X")
        output.append("3. Standard errors and confidence intervals from DebiasedLasso")
        output.append("4. Significant coefficients indicate treatment effect moderators")
        
        return "\n".join(output)