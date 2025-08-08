import re
from logger_base import get_logger


exercise = """

@content {

    apple  = red;
    pear   = green;
    grape  = purple;
    banana = yellow;
    = [blank, white];

}

"""

#

def extract_content_blocks(s, single=True):
     found = re.findall(r"@content\s*.*?{(.*?)}", self.data, re.DOTALL)

     if single and len(found) > 1:
         print("Didn't find anything worthy bro")
         return None





