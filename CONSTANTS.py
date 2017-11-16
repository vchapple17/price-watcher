class CONSTANTS:
    _filename = "flight_log.csv"
    _jobFilename = "job-details.txt"
    _jobFileNumCols = 4

    # def __init__(self):
    #     return
    #
    @staticmethod
    def FLIGHT_FILENAME():
        return CONSTANTS._filename
    @staticmethod
    def JOB_DETAILS_FILENAME():
        return CONSTANTS._jobFilename
    @staticmethod
    def JOB_DETAILS_NUM_COLS():
        return CONSTANTS._jobFileNumCols
