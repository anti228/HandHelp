# region Imports
from inspect import stack

import lib
from lib_io import *
import log
# endregion Imports


# region MainCode
def main():
    """"""
    logger.info("[Start script]")

    lib.deleteContentOfFolder(lib.OUTPUT_FOLDER_LST)

    # fileName = "test-10-chunks.html"
    # fileName = "test-100-chunks.html"
    # fileName = "test-1000-chunks.html"

    # fileName = "doc_1-11499.html"
    fileName = "doc_11500-13157.html"
    

    # Read file
    # linesLst = lib.readFileAsLinesLst(fileName, encoding="ascii")
    # linesLst = lib.readFileAsLinesLst(fileName, encoding="latin-1")
    linesLst = lib.readFileAsLinesLst(fileName, encoding="Windows-1251")

    
    # Get chunks
    chunksLst = lib.linesLstToChunksLst(linesLst)
    if not chunksLst:
        logger.warn("chunksLst is empty!")
        return
    
    logger.info(f"File {fileName} is loaded.")
    

    # Parse chunks
    parsedChunksLst = []
    for chunk in chunksLst:
        parsedChunk = lib.parseChunk(chunk)
        if parsedChunk:
            parsedChunksLst.append(parsedChunk)
    

    # Write chunks to files
    # lib.writeObjsToFilesWithTSname(chunksLst, filePath=lib.OUTPUT_FOLDER_LST)


    # Write chunks to files (splited on successed and failed)
    # successParsedChunks = list()
    # problemParsedChunks = list()
    # for parsedChunk in parsedChunksLst:
    #     if not parsedChunk["raw_text_rest"]:
    #         del parsedChunk["raw_text_rest"]
    #         itemToBeWrited = {
    #             "content" : parsedChunk
    #             ,"name" : "SUCCESS"
    #             ,"path" : lib.OUTPUT_FOLDER_LST
    #             ,"timestamp": True
    #         }
    #         successParsedChunks.append(itemToBeWrited)
    #     else:
    #         itemToBeWrited = {
    #             "content" : parsedChunk
    #             ,"name" : "FAIL"
    #             ,"path" : lib.OUTPUT_FOLDER_LST
    #             ,"timestamp": True
    #         }
    #         problemParsedChunks.append(itemToBeWrited)

    # lib.writeObjsToFiles(successParsedChunks)
    # lib.writeObjsToFiles(problemParsedChunks)


    # Write chunks to files
    tableName = "simple_data"
    colName = "id"
    seqName = f"{tableName}_{colName}_seq"
    query = """
        INSERT INTO simple_data (
            raw_text, question_number, who_asks, tags, question, who_answers, answer, answer_date, raw_text_rest
        )
        VALUES (
            %(raw_text)s, %(question_number)s, %(who_asks)s, %(tags)s, %(question)s, %(who_answers)s, %(answer)s, %(answer_date)s, %(raw_text_rest)s
        ) returning id
    """

    # Drop seq
    # result = lib.alterSeq(seqName, 1)
    # if not result:
    #     return
    
    # Trunc table
    # result = lib.truncateTable(tableName)
    # if not result:
    #     return
    
 
    for parsedChunk in parsedChunksLst:
        result = lib.insert(query, parsedChunk)
        if result:
            logger.info(f"Inserted row {result}")


    logger.info("[End script]")
# endregion MainCode


#region Startup
logger = log.init()
if __name__=="__main__":
    if logger:
        logger.info(f"This module is executing")
        main()
else:
    logger.info(f"This module is imported")
#endregion Startup