"""
Main lawkit wrapper implementation
"""

import json
import subprocess
import tempfile
import os
import platform
import sys
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Literal
from dataclasses import dataclass


# Type definitions
Format = Literal["text", "json", "csv", "yaml", "toml", "xml"]
OutputFormat = Literal["text", "json", "csv", "yaml", "toml", "xml"]
LawType = Literal["benf", "pareto", "zipf", "normal", "poisson"]


@dataclass
class LawkitOptions:
    """Options for lawkit operations"""
    # Common options
    format: Optional[Format] = None
    quiet: bool = False
    verbose: bool = False
    filter: Optional[str] = None
    min_count: Optional[int] = None
    
    # Integration options
    laws: Optional[str] = None  # "benf,pareto,zipf,normal,poisson"
    focus: Optional[str] = None  # "quality", "concentration", "distribution", "anomaly"
    threshold: Optional[float] = None  # Analysis threshold for anomaly detection
    recommend: bool = False
    report: Optional[str] = None  # "summary", "detailed", "anomalies"
    consistency_check: bool = False
    cross_validation: bool = False
    confidence_level: Optional[float] = None
    purpose: Optional[str] = None  # "quality", "fraud", "concentration", "anomaly", "distribution", "general"
    
    # Benford-specific options
    threshold_level: Optional[str] = None  # "low", "medium", "high", "critical", "auto"
    confidence: Optional[float] = None  # Statistical confidence level (0.01-0.99)
    sample_size: Optional[int] = None  # Maximum sample size for large datasets
    min_value: Optional[float] = None  # Minimum value to include in analysis
    
    # Pareto-specific options
    concentration: Optional[float] = None
    gini_coefficient: bool = False
    percentiles: Optional[str] = None
    business_analysis: bool = False
    
    # Zipf-specific options
    text: bool = False  # Enable text analysis mode
    words: Optional[int] = None  # Maximum number of words to analyze in text mode
    vocabulary_size: Optional[int] = None  # Vocabulary size for text generation
    exponent: Optional[float] = None  # Zipf exponent
    
    # Normal distribution options
    test: Optional[str] = None  # Normality test method
    outliers: bool = False  # Enable outlier detection
    outlier_method: Optional[str] = None  # Outlier detection method
    quality_control: bool = False  # Enable quality control analysis
    spec_limits: Optional[str] = None  # Specification limits for quality control
    enable_timeseries: bool = False  # Enable time series analysis
    timeseries_window: Optional[int] = None  # Time series analysis window size
    mean: Optional[float] = None  # Mean of normal distribution
    stddev: Optional[float] = None  # Standard deviation of normal distribution
    
    # Poisson distribution options
    predict: bool = False  # Enable probability prediction
    max_events: Optional[int] = None  # Maximum number of events for analysis
    rare_events: bool = False  # Focus on rare event analysis
    lambda_: Optional[float] = None  # Lambda parameter for Poisson distribution (lambda is a keyword)
    time_series: bool = False  # Generate time-series event data
    
    # Generation options
    samples: Optional[int] = None
    seed: Optional[int] = None
    output_file: Optional[str] = None
    fraud_rate: Optional[float] = None
    range: Optional[str] = None  # "1,100000"
    scale: Optional[float] = None


class LawkitResult:
    """Result of a lawkit analysis operation"""
    def __init__(self, data: Dict[str, Any], law_type: str):
        self.data = data
        self.law_type = law_type
    
    @property
    def risk_level(self) -> Optional[str]:
        """Get risk level if present"""
        return self.data.get("risk_level")
    
    @property
    def p_value(self) -> Optional[float]:
        """Get p-value if present"""
        return self.data.get("p_value")
    
    @property
    def chi_square(self) -> Optional[float]:
        """Get chi-square statistic if present"""
        return self.data.get("chi_square")
    
    @property
    def mad(self) -> Optional[float]:
        """Get Mean Absolute Deviation if present"""
        return self.data.get("mad")
    
    @property
    def gini_coefficient(self) -> Optional[float]:
        """Get Gini coefficient if present"""
        return self.data.get("gini_coefficient")
    
    @property
    def concentration_80_20(self) -> Optional[float]:
        """Get 80/20 concentration if present"""
        return self.data.get("concentration_80_20")
    
    @property
    def exponent(self) -> Optional[float]:
        """Get Zipf exponent if present"""
        return self.data.get("exponent")
    
    @property
    def lambda_estimate(self) -> Optional[float]:
        """Get lambda estimate for Poisson distribution if present"""
        return self.data.get("lambda")
    
    @property
    def mean(self) -> Optional[float]:
        """Get mean if present"""
        return self.data.get("mean")
    
    @property
    def std_dev(self) -> Optional[float]:
        """Get standard deviation if present"""
        return self.data.get("std_dev")
    
    @property
    def outliers(self) -> Optional[List[Any]]:
        """Get outliers if present"""
        return self.data.get("outliers")
    
    @property
    def anomalies(self) -> Optional[List[Any]]:
        """Get anomalies if present"""  
        return self.data.get("anomalies")
    
    def __repr__(self) -> str:
        return f"LawkitResult(law_type='{self.law_type}', data={self.data})"


class LawkitError(Exception):
    """Error thrown when lawkit command fails"""
    def __init__(self, message: str, exit_code: int, stderr: str):
        super().__init__(message)
        self.exit_code = exit_code
        self.stderr = stderr


def _get_lawkit_binary_path() -> str:
    """Get the path to the lawkit binary (embedded in wheel)"""
    import sysconfig
    
    binary_name = "lawkit.exe" if platform.system() == "Windows" else "lawkit"
    
    # Check if binary exists in the package installation
    if hasattr(sys, "_MEIPASS"):  # PyInstaller
        binary_path = Path(sys._MEIPASS) / binary_name
        if binary_path.exists():
            return str(binary_path)
    
    # Try sysconfig scripts path (most reliable for pip installs)
    try:
        scripts_path = Path(sysconfig.get_path("scripts")) / binary_name
        if scripts_path.exists():
            return str(scripts_path)
    except (KeyError, TypeError):
        pass
    
    # Try user scheme detection for user installs
    try:
        if sys.version_info >= (3, 10):
            user_scheme = sysconfig.get_preferred_scheme("user")
        else:
            user_scheme = "posix_user" if os.name == "posix" else "nt_user"
        
        user_scripts = Path(sysconfig.get_path("scripts", scheme=user_scheme)) / binary_name
        if user_scripts.exists():
            return str(user_scripts)
    except (KeyError, TypeError):
        pass
    
    # Try package relative paths
    package_dir = Path(__file__).parent.parent.parent
    for relative_path in [
        package_dir / "bin" / binary_name,
        package_dir / ".." / "bin" / binary_name,
        package_dir / ".." / ".." / "bin" / binary_name,
        Path(__file__).parent / binary_name,
    ]:
        if relative_path.exists():
            return str(relative_path)
    
    # Fall back to system PATH
    return "lawkit"


def _execute_lawkit(args: List[str]) -> tuple[str, str]:
    """Execute lawkit command and return stdout, stderr"""
    lawkit_path = _get_lawkit_binary_path()
    
    try:
        result = subprocess.run(
            [lawkit_path] + args,
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        # Exit codes 10-19 are typically warnings, not fatal errors
        if result.returncode == 0 or (result.returncode >= 10 and result.returncode <= 19):
            return result.stdout, result.stderr
        
        raise LawkitError(
            f"lawkit exited with code {result.returncode}",
            result.returncode,
            result.stderr or ""
        )
    except FileNotFoundError:
        raise LawkitError(
            "lawkit command not found. Please install lawkit CLI tool.",
            -1,
            ""
        )


def analyze_benford(
    input_data: str,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Analyze data using Benford's Law
    
    Args:
        input_data: Path to input file or '-' for stdin
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> result = analyze_benford('financial_data.csv')
        >>> print(result)
        
        >>> json_result = analyze_benford('accounting.json', 
        ...                              LawkitOptions(format='json', output='json'))
        >>> print(f"Risk level: {json_result.risk_level}")
        >>> print(f"P-value: {json_result.p_value}")
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["benf", input_data]
    
    # Add all options
    _add_common_options(args, options)
    
    stdout, stderr = _execute_lawkit(args)
    
    # If output format is JSON, parse the result
    if options.format == "json":
        try:
            json_data = json.loads(stdout)
            return LawkitResult(json_data, "benford")
        except json.JSONDecodeError as e:
            raise LawkitError(f"Failed to parse JSON output: {e}", -1, "")
    
    # Return raw output for other formats
    return stdout


def analyze_pareto(
    input_data: str,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Analyze data using Pareto principle (80/20 rule)
    
    Args:
        input_data: Path to input file or '-' for stdin
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> result = analyze_pareto('sales_data.csv')
        >>> print(result)
        
        >>> json_result = analyze_pareto('revenue.json', 
        ...                             LawkitOptions(output='json', gini_coefficient=True))
        >>> print(f"Gini coefficient: {json_result.gini_coefficient}")
        >>> print(f"80/20 concentration: {json_result.concentration_80_20}")
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["pareto", input_data]
    
    # Add all options
    _add_common_options(args, options)
    
    stdout, stderr = _execute_lawkit(args)
    
    # If output format is JSON, parse the result
    if options.format == "json":
        try:
            json_data = json.loads(stdout)
            return LawkitResult(json_data, "pareto")
        except json.JSONDecodeError as e:
            raise LawkitError(f"Failed to parse JSON output: {e}", -1, "")
    
    # Return raw output for other formats
    return stdout


def analyze_zipf(
    input_data: str,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Analyze data using Zipf's Law
    
    Args:
        input_data: Path to input file or '-' for stdin
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> result = analyze_zipf('text_data.txt')
        >>> print(result)
        
        >>> json_result = analyze_zipf('word_frequencies.json', 
        ...                          LawkitOptions(output='json'))
        >>> print(f"Zipf exponent: {json_result.exponent}")
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["zipf", input_data]
    
    # Add all options
    _add_common_options(args, options)
    
    stdout, stderr = _execute_lawkit(args)
    
    # If output format is JSON, parse the result
    if options.format == "json":
        try:
            json_data = json.loads(stdout)
            return LawkitResult(json_data, "zipf")
        except json.JSONDecodeError as e:
            raise LawkitError(f"Failed to parse JSON output: {e}", -1, "")
    
    # Return raw output for other formats
    return stdout


def analyze_normal(
    input_data: str,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Analyze data for normal distribution
    
    Args:
        input_data: Path to input file or '-' for stdin
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> result = analyze_normal('measurements.csv')
        >>> print(result)
        
        >>> json_result = analyze_normal('quality_data.json', 
        ...                             LawkitOptions(output='json', outlier_detection=True))
        >>> print(f"Mean: {json_result.mean}")
        >>> print(f"Standard deviation: {json_result.std_dev}")
        >>> print(f"Outliers: {json_result.outliers}")
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["normal", input_data]
    
    # Add all options
    _add_common_options(args, options)
    
    stdout, stderr = _execute_lawkit(args)
    
    # If output format is JSON, parse the result
    if options.format == "json":
        try:
            json_data = json.loads(stdout)
            return LawkitResult(json_data, "normal")
        except json.JSONDecodeError as e:
            raise LawkitError(f"Failed to parse JSON output: {e}", -1, "")
    
    # Return raw output for other formats
    return stdout


def analyze_poisson(
    input_data: str,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Analyze data using Poisson distribution
    
    Args:
        input_data: Path to input file or '-' for stdin
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> result = analyze_poisson('event_counts.csv')
        >>> print(result)
        
        >>> json_result = analyze_poisson('incidents.json', 
        ...                              LawkitOptions(output='json'))
        >>> print(f"Lambda estimate: {json_result.lambda_estimate}")
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["poisson", input_data]
    
    # Add all options
    _add_common_options(args, options)
    
    stdout, stderr = _execute_lawkit(args)
    
    # If output format is JSON, parse the result
    if options.format == "json":
        try:
            json_data = json.loads(stdout)
            return LawkitResult(json_data, "poisson")
        except json.JSONDecodeError as e:
            raise LawkitError(f"Failed to parse JSON output: {e}", -1, "")
    
    # Return raw output for other formats
    return stdout


def analyze_laws(
    input_data: str,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Analyze data using multiple statistical laws (basic analysis)
    
    Args:
        input_data: Path to input file or '-' for stdin
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> result = analyze_laws('dataset.csv')
        >>> print(result)
        
        >>> json_result = analyze_laws('complex_data.json', 
        ...                          LawkitOptions(format='json'))
        >>> print(f"Risk level: {json_result.risk_level}")
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["analyze", input_data]
    
    # Add common options
    _add_common_options(args, options)
    
    stdout, stderr = _execute_lawkit(args)
    
    # If output format is JSON, parse the result
    if options.format == "json":
        try:
            json_data = json.loads(stdout)
            return LawkitResult(json_data, "analyze")
        except json.JSONDecodeError as e:
            raise LawkitError(f"Failed to parse JSON output: {e}", -1, "")
    
    # Return raw output for other formats
    return stdout


def validate_laws(
    input_data: str,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Validate data consistency using multiple statistical laws
    
    Args:
        input_data: Path to input file or '-' for stdin
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> result = validate_laws('dataset.csv')
        >>> print(result)
        
        >>> json_result = validate_laws('complex_data.json', 
        ...                           LawkitOptions(format='json'))
        >>> print(f"Validation result: {json_result.data}")
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["validate", input_data]
    
    # Add common options
    _add_common_options(args, options)
    
    stdout, stderr = _execute_lawkit(args)
    
    # If output format is JSON, parse the result
    if options.format == "json":
        try:
            json_data = json.loads(stdout)
            return LawkitResult(json_data, "validate")
        except json.JSONDecodeError as e:
            raise LawkitError(f"Failed to parse JSON output: {e}", -1, "")
    
    # Return raw output for other formats
    return stdout


def diagnose_laws(
    input_data: str,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Diagnose conflicts and generate detailed analysis report
    
    Args:
        input_data: Path to input file or '-' for stdin
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> result = diagnose_laws('dataset.csv')
        >>> print(result)
        
        >>> json_result = diagnose_laws('complex_data.json', 
        ...                           LawkitOptions(format='json'))
        >>> print(f"Diagnosis: {json_result.data}")
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["diagnose", input_data]
    
    # Add common options
    _add_common_options(args, options)
    
    stdout, stderr = _execute_lawkit(args)
    
    # If output format is JSON, parse the result
    if options.format == "json":
        try:
            json_data = json.loads(stdout)
            return LawkitResult(json_data, "diagnose")
        except json.JSONDecodeError as e:
            raise LawkitError(f"Failed to parse JSON output: {e}", -1, "")
    
    # Return raw output for other formats
    return stdout


# Backward compatibility alias
compare_laws = analyze_laws


def generate_data(
    law_type: LawType,
    options: Optional[LawkitOptions] = None,
    **kwargs
) -> str:
    """
    Generate sample data following a specific statistical law
    
    Args:
        law_type: Type of statistical law to use
        options: Generation options (samples, seed, etc.)
        **kwargs: Law-specific parameters (deprecated, use options instead)
        
    Returns:
        Generated data as string
        
    Examples:
        >>> data = generate_data('benf', LawkitOptions(samples=1000, seed=42))
        >>> print(data)
        
        >>> options = LawkitOptions(samples=500, fraud_rate=0.1, range="1,10000")
        >>> normal_data = generate_data('normal', options)
        >>> pareto_data = generate_data('pareto', LawkitOptions(concentration=0.8))
    """
    if options is None:
        options = LawkitOptions()
    
    args = ["generate", law_type]
    
    # Add all options
    _add_common_options(args, options)
    
    # Add law-specific parameters (backward compatibility)
    for key, value in kwargs.items():
        key_formatted = key.replace("_", "-")
        args.extend([f"--{key_formatted}", str(value)])
    
    stdout, stderr = _execute_lawkit(args)
    return stdout


def analyze_string(
    content: str,
    law_type: LawType,
    options: Optional[LawkitOptions] = None
) -> Union[str, LawkitResult]:
    """
    Analyze string data directly (writes to temporary file)
    
    Args:
        content: Data content as string
        law_type: Type of statistical law to use
        options: Analysis options
        
    Returns:
        String output for text format, or LawkitResult for JSON format
        
    Examples:
        >>> csv_data = "amount\\n123\\n456\\n789"
        >>> result = analyze_string(csv_data, 'benf', 
        ...                        LawkitOptions(format='csv', output='json'))
        >>> print(result.risk_level)
    """
    if options is None:
        options = LawkitOptions()
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Analyze the temporary file
        if law_type == "benf":
            return analyze_benford(tmp_file_path, options)
        elif law_type == "pareto":
            return analyze_pareto(tmp_file_path, options)
        elif law_type == "zipf":
            return analyze_zipf(tmp_file_path, options)
        elif law_type == "normal":
            return analyze_normal(tmp_file_path, options)
        elif law_type == "poisson":
            return analyze_poisson(tmp_file_path, options)
        else:
            raise LawkitError(f"Unknown law type: {law_type}", -1, "")
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)


def _add_common_options(args: List[str], options: LawkitOptions) -> None:
    """Add all options to command arguments"""
    # Common options
    if options.format:
        args.extend(["--format", options.format])
    if options.quiet:
        args.append("--quiet")
    if options.verbose:
        args.append("--verbose")
    if options.filter:
        args.extend(["--filter", options.filter])
    if options.min_count is not None:
        args.extend(["--min-count", str(options.min_count)])
    
    # Integration options
    if options.laws:
        args.extend(["--laws", options.laws])
    if options.focus:
        args.extend(["--focus", options.focus])
    if options.threshold is not None:
        args.extend(["--threshold", str(options.threshold)])
    if options.recommend:
        args.append("--recommend")
    if options.report:
        args.extend(["--report", options.report])
    if options.consistency_check:
        args.append("--consistency-check")
    if options.cross_validation:
        args.append("--cross-validation")
    if options.confidence_level is not None:
        args.extend(["--confidence-level", str(options.confidence_level)])
    if options.purpose:
        args.extend(["--purpose", options.purpose])
    
    # Benford-specific options
    if options.threshold_level:
        args.extend(["--threshold", options.threshold_level])
    if options.confidence is not None:
        args.extend(["--confidence", str(options.confidence)])
    if options.sample_size is not None:
        args.extend(["--sample-size", str(options.sample_size)])
    if options.min_value is not None:
        args.extend(["--min-value", str(options.min_value)])
    
    # Pareto-specific options
    if options.concentration is not None:
        args.extend(["--concentration", str(options.concentration)])
    if options.gini_coefficient:
        args.append("--gini-coefficient")
    if options.percentiles:
        args.extend(["--percentiles", options.percentiles])
    if options.business_analysis:
        args.append("--business-analysis")
    
    # Zipf-specific options
    if options.text:
        args.append("--text")
    if options.words is not None:
        args.extend(["--words", str(options.words)])
    if options.vocabulary_size is not None:
        args.extend(["--vocabulary-size", str(options.vocabulary_size)])
    if options.exponent is not None:
        args.extend(["--exponent", str(options.exponent)])
    
    # Normal distribution options
    if options.test:
        args.extend(["--test", options.test])
    if options.outliers:
        args.append("--outliers")
    if options.outlier_method:
        args.extend(["--outlier-method", options.outlier_method])
    if options.quality_control:
        args.append("--quality-control")
    if options.spec_limits:
        args.extend(["--spec-limits", options.spec_limits])
    if options.enable_timeseries:
        args.append("--enable-timeseries")
    if options.timeseries_window is not None:
        args.extend(["--timeseries-window", str(options.timeseries_window)])
    if options.mean is not None:
        args.extend(["--mean", str(options.mean)])
    if options.stddev is not None:
        args.extend(["--stddev", str(options.stddev)])
    
    # Poisson distribution options
    if options.predict:
        args.append("--predict")
    if options.max_events is not None:
        args.extend(["--max-events", str(options.max_events)])
    if options.rare_events:
        args.append("--rare-events")
    if options.lambda_ is not None:
        args.extend(["--lambda", str(options.lambda_)])
    if options.time_series:
        args.append("--time-series")
    
    # Generation options
    if options.samples is not None:
        args.extend(["--samples", str(options.samples)])
    if options.seed is not None:
        args.extend(["--seed", str(options.seed)])
    if options.output_file:
        args.extend(["--output-file", options.output_file])
    if options.fraud_rate is not None:
        args.extend(["--fraud-rate", str(options.fraud_rate)])
    if options.range:
        args.extend(["--range", options.range])
    if options.scale is not None:
        args.extend(["--scale", str(options.scale)])


def is_lawkit_available() -> bool:
    """
    Check if lawkit command is available in the system
    
    Returns:
        True if lawkit is available, False otherwise
        
    Examples:
        >>> if not is_lawkit_available():
        ...     print("Please install lawkit CLI tool")
        ...     exit(1)
    """
    try:
        _execute_lawkit(["--version"])
        return True
    except LawkitError:
        return False


def get_version() -> str:
    """
    Get the version of the lawkit CLI tool
    
    Returns:
        Version string
        
    Examples:
        >>> version = get_version()
        >>> print(f"Using lawkit version: {version}")
    """
    try:
        stdout, stderr = _execute_lawkit(["--version"])
        return stdout.strip()
    except LawkitError:
        return "Unknown"


def selftest() -> bool:
    """
    Run lawkit self-test to verify installation
    
    Returns:
        True if self-test passes, False otherwise
        
    Examples:
        >>> if not selftest():
        ...     print("lawkit self-test failed")
        ...     exit(1)
    """
    try:
        _execute_lawkit(["selftest"])
        return True
    except LawkitError:
        return False