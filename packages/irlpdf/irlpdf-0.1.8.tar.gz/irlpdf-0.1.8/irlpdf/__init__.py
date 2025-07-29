

__app_name__ = "irlpdf"
__version__ = "0.1.8"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
   
) = range(3)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
}