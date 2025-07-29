import sys

from datetime import datetime
from .base_handler import  BaseHandler
from ..version import __version__

class StreamHandler(BaseHandler):
    '''
    Handles writing to streams
    '''
    def __init__(self,level):
        super().__init__()
        self.level=level
        self.start_logging()
        
    def start_logging(self):
        '''
        Begin logging with timestamp
        '''
        now = datetime.now()
        timestamp=now.strftime("%m/%d/%Y, %H:%M:%S")
        log_text=f"""---Log Start--- AEA Python-SDK {__version__} --- {timestamp}\n"""
        dashes = "-" * 80 + '\n'

        self.write_to_stream(log_text)
        self.write_to_stream(dashes);
        self.write_to_stream("AEA App Core Starting".rjust(len(dashes) - 2) + '\n');
        self.write_to_stream(dashes);
        
    def heading(self,frameinfo,message):
        '''
        Write heading
        '''
        data=self.text_to_heading(frameinfo,message)
        stream=sys.stdout
        self.write_to_stream(data,stream)
