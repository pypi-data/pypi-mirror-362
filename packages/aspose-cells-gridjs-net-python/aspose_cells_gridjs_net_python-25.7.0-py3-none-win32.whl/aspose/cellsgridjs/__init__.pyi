"""This is a wrapper module for Aspose.Cells.GridJs .NET assembly"""

from typing import Any

def get_pyinstaller_hook_dirs() -> Any:
  """Function required by PyInstaller. Returns paths to module 
  PyInstaller hooks. Not intended to be called explicitly."""
    ...

from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import aspose.cellsgridjs

class Config:
    '''Represents all the static settings for GridJs'''
    
    @overload
    @staticmethod
    def set_license(license_name : str):
        '''Licenses the component.
        
        :param license_name: Can be a full or short file name or name of an embedded resource.
        Use an empty string to switch to evaluation mode.'''
        ...
    
    @overload
    @staticmethod
    def set_license(stream : io.RawIOBase):
        '''Licenses the component.
        
        :param stream: A stream that contains the license.'''
        ...
    
    @staticmethod
    def set_font_folder(font_folder : strrecursive : bool):
        '''Sets the fonts folder
        
        :param font_folder: The folder that contains TrueType fonts.
        :param recursive: Determines whether or not to scan subfolders.'''
        ...
    
    @staticmethod
    def set_font_folders(font_folders : List[str]recursive : bool):
        '''Sets the fonts folders
        
        :param font_folders: The folders that contains TrueType fonts.
        :param recursive: Determines whether or not to scan subfolders.'''
        ...
    
    @classmethod
    @property
    def save_html_as_zip(cls) -> bool:
        ...
    
    @classmethod
    @save_html_as_zip.setter
    def save_html_as_zip(cls, value : bool):
        ...
    
    @classmethod
    @property
    def skip_invisible_shapes(cls) -> bool:
        ...
    
    @classmethod
    @skip_invisible_shapes.setter
    def skip_invisible_shapes(cls, value : bool):
        ...
    
    @classmethod
    @property
    def lazy_loading(cls) -> bool:
        ...
    
    @classmethod
    @lazy_loading.setter
    def lazy_loading(cls, value : bool):
        ...
    
    @classmethod
    @property
    def same_image_detecting(cls) -> bool:
        ...
    
    @classmethod
    @same_image_detecting.setter
    def same_image_detecting(cls, value : bool):
        ...
    
    @classmethod
    @property
    def auto_optimize_for_large_cells(cls) -> bool:
        ...
    
    @classmethod
    @auto_optimize_for_large_cells.setter
    def auto_optimize_for_large_cells(cls, value : bool):
        ...
    
    @classmethod
    @property
    def islimit_shape_or_image(cls) -> bool:
        ...
    
    @classmethod
    @islimit_shape_or_image.setter
    def islimit_shape_or_image(cls, value : bool):
        ...
    
    @classmethod
    @property
    def max_shape_or_image_count(cls) -> int:
        ...
    
    @classmethod
    @max_shape_or_image_count.setter
    def max_shape_or_image_count(cls, value : int):
        ...
    
    @classmethod
    @property
    def max_total_shape_or_image_count(cls) -> int:
        ...
    
    @classmethod
    @max_total_shape_or_image_count.setter
    def max_total_shape_or_image_count(cls, value : int):
        ...
    
    @classmethod
    @property
    def max_shape_or_image_width_or_height(cls) -> int:
        ...
    
    @classmethod
    @max_shape_or_image_width_or_height.setter
    def max_shape_or_image_width_or_height(cls, value : int):
        ...
    
    @classmethod
    @property
    def max_pdf_save_seconds(cls) -> int:
        ...
    
    @classmethod
    @max_pdf_save_seconds.setter
    def max_pdf_save_seconds(cls, value : int):
        ...
    
    @classmethod
    @property
    def ignore_empty_content(cls) -> bool:
        ...
    
    @classmethod
    @ignore_empty_content.setter
    def ignore_empty_content(cls, value : bool):
        ...
    
    @classmethod
    @property
    def use_print_area(cls) -> bool:
        ...
    
    @classmethod
    @use_print_area.setter
    def use_print_area(cls, value : bool):
        ...
    
    @classmethod
    @property
    def is_collaborative(cls) -> bool:
        ...
    
    @classmethod
    @is_collaborative.setter
    def is_collaborative(cls, value : bool):
        ...
    
    @classmethod
    @property
    def load_time_out(cls) -> int:
        ...
    
    @classmethod
    @load_time_out.setter
    def load_time_out(cls, value : int):
        ...
    
    @classmethod
    @property
    def show_chart_sheet(cls) -> bool:
        ...
    
    @classmethod
    @show_chart_sheet.setter
    def show_chart_sheet(cls, value : bool):
        ...
    
    @classmethod
    @property
    def empty_sheet_max_row(cls) -> int:
        ...
    
    @classmethod
    @empty_sheet_max_row.setter
    def empty_sheet_max_row(cls, value : int):
        ...
    
    @classmethod
    @property
    def empty_sheet_max_col(cls) -> int:
        ...
    
    @classmethod
    @empty_sheet_max_col.setter
    def empty_sheet_max_col(cls, value : int):
        ...
    
    @classmethod
    @property
    def picture_cache_directory(cls) -> str:
        ...
    
    @classmethod
    @picture_cache_directory.setter
    def picture_cache_directory(cls, value : str):
        ...
    
    @classmethod
    @property
    def file_cache_directory(cls) -> str:
        ...
    
    @classmethod
    @file_cache_directory.setter
    def file_cache_directory(cls, value : str):
        ...
    
    @classmethod
    @property
    def base_route_name(cls) -> str:
        ...
    
    @classmethod
    @base_route_name.setter
    def base_route_name(cls, value : str):
        ...
    
    ...

class GridAbstractCalculationEngine:
    '''Represents user's custom calculation engine to extend the default calculation engine of Aspose.Cells.'''
    
    def calculate(self, data : aspose.cellsgridjs.GridCalculationData):
        '''Calculates one function with given data.
        
        :param data: The required data to calculate function such as function name, parameters, ...etc.'''
        ...
    
    ...

class GridCacheForStream:
    '''This class contains the cache operations for GridJs. User shall implement his own business logic for storage based on it..'''
    
    def save_stream(self, s : io.RawIOBase, uid : str):
        '''Implements this method to save cache,save the stream to the cache with the key uid.'''
        ...
    
    def load_stream(self, uid : str) -> io.RawIOBase:
        '''Implements this method to load cache with the key uid,return the stream from the cache.'''
        ...
    
    def is_existed(self, uid : str) -> bool:
        '''Checks whether the cache with uid is existed
        
        :param uid: The unique id for the file cache.
        :returns: The bool value'''
        ...
    
    def get_file_url(self, uid : str) -> str:
        '''Implements this method to get the file url  from the cache.
        
        :param uid: The unique id for the file cache.
        :returns: The URL of the file'''
        ...
    
    ...

class GridCalculationData:
    '''Represents the required data when calculating one function, such as function name, parameters, ...etc.'''
    
    def get_param_value(self, index : int) -> any:
        '''Gets the represented value object of the parameter at given index.
        
        :param index: The index of the parameter(0 based).
        :returns: If the parameter is plain value, then returns the plain value.
        If the parameter is reference, then return ReferredArea object.'''
        ...
    
    def get_param_text(self, index : int) -> str:
        '''Gets the literal text of the parameter at given index.
        
        :param index: The index of the parameter(0 based).
        :returns: The literal text of the parameter.'''
        ...
    
    @property
    def calculated_value(self) -> any:
        ...
    
    @calculated_value.setter
    def calculated_value(self, value : any):
        ...
    
    @property
    def row(self) -> int:
        '''Gets the Cell Row index where the function is in.'''
        ...
    
    @property
    def column(self) -> int:
        '''Gets the Cell Column index where the function is in.'''
        ...
    
    @property
    def string_value(self) -> str:
        ...
    
    @property
    def value(self) -> any:
        '''Gets the Cell value where the function is in.'''
        ...
    
    @property
    def formula(self) -> str:
        '''Gets the Cell formula where the function is in.'''
        ...
    
    @property
    def sheet_name(self) -> str:
        ...
    
    @property
    def function_name(self) -> str:
        ...
    
    @property
    def param_count(self) -> int:
        ...
    
    ...

class GridCellException:
    '''The exception that is thrown when GridJs specified error occurs.'''
    
    def to_string(self) -> str:
        '''Creates and returns a string representation of the current exception.'''
        ...
    
    @property
    def code(self) -> aspose.cellsgridjs.GridExceptionType:
        '''Represents the exception code.'''
        ...
    
    ...

class GridJsControllerBase:
    
    ...

class GridJsOptions:
    '''Represents  all the load options for GridJs'''
    
    @property
    def save_html_as_zip(self) -> bool:
        ...
    
    @save_html_as_zip.setter
    def save_html_as_zip(self, value : bool):
        ...
    
    @property
    def skip_invisible_shapes(self) -> bool:
        ...
    
    @skip_invisible_shapes.setter
    def skip_invisible_shapes(self, value : bool):
        ...
    
    @property
    def lazy_loading(self) -> bool:
        ...
    
    @lazy_loading.setter
    def lazy_loading(self, value : bool):
        ...
    
    @property
    def same_image_detecting(self) -> bool:
        ...
    
    @same_image_detecting.setter
    def same_image_detecting(self, value : bool):
        ...
    
    @property
    def auto_optimize_for_large_cells(self) -> bool:
        ...
    
    @auto_optimize_for_large_cells.setter
    def auto_optimize_for_large_cells(self, value : bool):
        ...
    
    @property
    def islimit_shape_or_image(self) -> bool:
        ...
    
    @islimit_shape_or_image.setter
    def islimit_shape_or_image(self, value : bool):
        ...
    
    @property
    def max_shape_or_image_count(self) -> int:
        ...
    
    @max_shape_or_image_count.setter
    def max_shape_or_image_count(self, value : int):
        ...
    
    @property
    def max_total_shape_or_image_count(self) -> int:
        ...
    
    @max_total_shape_or_image_count.setter
    def max_total_shape_or_image_count(self, value : int):
        ...
    
    @property
    def max_shape_or_image_width_or_height(self) -> int:
        ...
    
    @max_shape_or_image_width_or_height.setter
    def max_shape_or_image_width_or_height(self, value : int):
        ...
    
    @property
    def max_pdf_save_seconds(self) -> int:
        ...
    
    @max_pdf_save_seconds.setter
    def max_pdf_save_seconds(self, value : int):
        ...
    
    @property
    def ignore_empty_content(self) -> bool:
        ...
    
    @ignore_empty_content.setter
    def ignore_empty_content(self, value : bool):
        ...
    
    @property
    def use_print_area(self) -> bool:
        ...
    
    @use_print_area.setter
    def use_print_area(self, value : bool):
        ...
    
    @property
    def is_collaborative(self) -> bool:
        ...
    
    @is_collaborative.setter
    def is_collaborative(self, value : bool):
        ...
    
    @property
    def load_time_out(self) -> int:
        ...
    
    @load_time_out.setter
    def load_time_out(self, value : int):
        ...
    
    @property
    def show_chart_sheet(self) -> bool:
        ...
    
    @show_chart_sheet.setter
    def show_chart_sheet(self, value : bool):
        ...
    
    @property
    def empty_sheet_max_row(self) -> int:
        ...
    
    @empty_sheet_max_row.setter
    def empty_sheet_max_row(self, value : int):
        ...
    
    @property
    def empty_sheet_max_col(self) -> int:
        ...
    
    @empty_sheet_max_col.setter
    def empty_sheet_max_col(self, value : int):
        ...
    
    @property
    def picture_cache_directory(self) -> str:
        ...
    
    @picture_cache_directory.setter
    def picture_cache_directory(self, value : str):
        ...
    
    @property
    def file_cache_directory(self) -> str:
        ...
    
    @file_cache_directory.setter
    def file_cache_directory(self, value : str):
        ...
    
    @property
    def font_folders(self) -> List[str]:
        ...
    
    @font_folders.setter
    def font_folders(self, value : List[str]):
        ...
    
    @property
    def base_route_name(self) -> str:
        ...
    
    @base_route_name.setter
    def base_route_name(self, value : str):
        ...
    
    @property
    def cache_imp(self) -> aspose.cellsgridjs.GridCacheForStream:
        ...
    
    @cache_imp.setter
    def cache_imp(self, value : aspose.cellsgridjs.GridCacheForStream):
        ...
    
    ...

class GridJsService(IGridJsService):
    '''Provides the basic operation apis used in controller actions.'''
    
    def check_in_cache_for_collaborative(self, uid : str) -> bool:
        '''Check wether workbook instance is in memory cache .this method is apply for Collaborative mode only.'''
        ...
    
    def update_cell(self, p : str, uid : str) -> str:
        '''Applies the update operation.
        
        :param p: The JSON format string of update operation.
        :param uid: The unique id for the file cache.
        :returns: The JSON format string of the update result.'''
        ...
    
    def detail_stream_json_with_uid(self, stream : io.RawIOBase, file_path : str, uid : str):
        '''Write the JSON string  for the file to the stream  by the specified unique id.
        
        :param stream: The stream that will be written
        :param file_path: The file path
        :param uid: The unique id for the file cache.'''
        ...
    
    def detail_stream_json(self, stream : io.RawIOBase, file_path : str):
        '''Write the JSON string  for the file to the stream .
        
        :param stream: The stream that will be written
        :param file_path: The file path'''
        ...
    
    def lazy_loading_stream_json(self, stream : io.RawIOBase, sheet_name : str, uid : str):
        '''Writes the JSON string of the specified sheet in the file from the cache using the specified unique id  to the stream..
        
        :param stream: The stream that will be written
        :param sheet_name: The sheet name.
        :param uid: The unique id for the file cache.'''
        ...
    
    def add_image_by_url(self, p : str, uid : str, imageurl : str) -> str:
        '''Applies the add image from remote URL operation.
        
        :param p: The JSON string parameter
        :param uid: The unique id for the file cache.
        :param imageurl: Specify the image URL.
        :returns: The JSON string result'''
        ...
    
    def copy_image(self, p : str, uid : str) -> str:
        '''Applies the copy image operation.
        
        :param p: The JSON string parameter
        :param uid: The unique id for the file cache.
        :returns: The JSON string result'''
        ...
    
    def load(self, uid : str, filename : str) -> str:
        '''Gets the JSON  string  of the file from the cache using the specified unique id,set the output filename in the JSON.
        
        :param uid: The unique id for the file cache.
        :param filename: Specifies the file name in the JSON. If set to null,the default filename is: book1.
        :returns: The JSON string'''
        ...
    
    def image(self, uid : str, picid : str) -> io.RawIOBase:
        '''Get Stream of image.
        
        :param uid: The unique id for the file cache.
        :param picid: The image id.
        :returns: The image stream'''
        ...
    
    def ole(self, uid : str, sheet : str, oleid : int, filename : Any) -> bytes:
        '''Gets the byte array data of the  embedded ole object .
        
        :param uid: The unique id for the file cache.
        :param oleid: The  id for the embedded ole object.
        :returns: The byte array data of the  embedded ole object .'''
        ...
    
    def image_url(self, base_url : str, picid : str, uid : str) -> str:
        '''Gets the image URL.
        
        :param base_url: The base action URL.
        :param picid: The image id.
        :param uid: The unique id for the file cache.
        :returns: The image URL'''
        ...
    
    def get_file(self, fileid : str) -> io.RawIOBase:
        '''Get file stream
        
        :param fileid: the file id
        :returns: The stream of the file'''
        ...
    
    def download(self, p : str, uid : str, filename : str) -> str:
        '''Applies the download file operation
        
        :param p: The JSON parameter
        :param uid: The unique id for the file cache.
        :param filename: The file name
        :returns: The file URL'''
        ...
    
    ...

class GridJsWorkbook:
    '''Represents the main entry class for GridJs'''
    
    @overload
    def import_excel_file(self, uid : str, file_name : str, password : str):
        '''Imports the excel file from file path and open password.
        
        :param uid: The unique id for the file cache, if set to null,it will be generated automatically.
        :param file_name: The full path of the file.
        :param password: The open password  of the excel file.The value can be null If no passowrd is set.'''
        ...
    
    @overload
    def import_excel_file(self, uid : str, file_name : str):
        '''Imports the excel file from the file path.
        
        :param uid: The unique id for the file cache, if set to null,it will be generated automatically.
        :param file_name: The full path of the file.'''
        ...
    
    @overload
    def import_excel_file(self, file_name : str):
        '''Imports the excel file from the file path.
        
        :param file_name: The full path of the file.'''
        ...
    
    @overload
    def import_excel_file(self, uid : str, filestream : io.RawIOBase, format : aspose.cellsgridjs.GridLoadFormat, password : str):
        '''Imports the excel file from  file stream with load format and open password.
        
        :param uid: The unique id for the file cache, if set to null,it will be generated automatically.
        :param filestream: The stream of the excel file .
        :param format: The LoadFormat of the excel file.
        :param password: The open password  of the excel file.The value can be null If no passowrd is set'''
        ...
    
    @overload
    def import_excel_file(self, uid : str, filestream : io.RawIOBase, format : aspose.cellsgridjs.GridLoadFormat):
        '''Imports the excel file from file stream.
        
        :param uid: The unique id for the file cache, if set to null,it will be generated automatically.
        :param filestream: The stream of the excel file .
        :param format: The LoadFormat of the excel file.'''
        ...
    
    @overload
    def import_excel_file(self, filestream : io.RawIOBase, format : aspose.cellsgridjs.GridLoadFormat, password : str):
        '''Imports the excel file from file stream with load format and open password.
        
        :param filestream: The stream of the excel file .
        :param format: The LoadFormat of the excel file.
        :param password: The open password  of the excel file.The value can be null If no passowrd is set.'''
        ...
    
    @overload
    def import_excel_file(self, filestream : io.RawIOBase, format : aspose.cellsgridjs.GridLoadFormat):
        '''Imports the excel file from file stream with load format.
        
        :param filestream: The stream of the excel file .
        :param format: The LoadFormat of the excel file.'''
        ...
    
    @overload
    def export_to_json(self, filename : str) -> str:
        '''Gets JSON  string from memory data,set the output filename in the JSON.
        
        :param filename: Specifies the file name in the JSON. If set to null,the default filename is: book1..
        :returns: The JSON string.'''
        ...
    
    @overload
    def export_to_json(self) -> str:
        '''Gets JSON string from memory data, the default filename in the JSON is: book1.
        
        :returns: The JSON string.'''
        ...
    
    @overload
    def save_to_excel_file(self, stream : io.RawIOBase):
        '''Saves the memory data to the sream, baseed on the origin file format.
        
        :param stream: The stream to save.'''
        ...
    
    @overload
    def save_to_excel_file(self, path : str):
        '''Saves the memory data to the file path,if the file has extension ,save format is baseed on the file extension .
        
        :param path: The file path to save.'''
        ...
    
    @overload
    def save_to_pdf(self, path : str):
        '''Saves the memory data to the file path,the save format is pdf.
        
        :param path: The file path to save.'''
        ...
    
    @overload
    def save_to_pdf(self, stream : io.RawIOBase):
        '''Saves the memory data to the sream,the save format is pdf.
        
        :param stream: The stream to save.'''
        ...
    
    @overload
    def save_to_xlsx(self, path : str):
        '''Saves the memory data to the file path,the save format is xlsx.
        
        :param path: The file path to save.'''
        ...
    
    @overload
    def save_to_xlsx(self, stream : io.RawIOBase):
        '''Saves the memory data to the sream,the save format is xlsx.
        
        :param stream: The stream to save.'''
        ...
    
    @overload
    def save_to_html(self, path : str):
        '''Saves the memory data to the file path,the save format is html.
        
        :param path: The file path to save.'''
        ...
    
    @overload
    def save_to_html(self, stream : io.RawIOBase):
        '''Saves the memory data to the sream,the save format is html
        
        :param stream: The stream to save.'''
        ...
    
    def json_to_stream_by_uid(self, stream : io.RawIOBase, uid : str, filename : str) -> bool:
        '''Retrieve the JSON string of the file from the cache using the specified unique id,set the output filename in the JSON,and write it to the stream.
        
        :param stream: The stream that will be written
        :param uid: The unique id for the file cache.
        :param filename: Specifies the file name in the JSON. If set to null,the default filename is: book1.'''
        ...
    
    def json_to_stream(self, stream : io.RawIOBase, filename : str):
        '''Retrieve the JSON string from memory data,set the output filename in the JSON, and write it to the stream.
        
        :param stream: The stream that will be written
        :param filename: Specifies the file name in the JSON. If set to null,the default filename is: book1.'''
        ...
    
    def lazy_loading_stream(self, stream : io.RawIOBase, uid : str, sheet_name : str):
        '''Retrieve the JSON string of the specified sheet in the file from the cache using the specified unique id, and write it to the stream.
        
        :param stream: The stream that will be written
        :param uid: The unique id for the file cache.
        :param sheet_name: the sheet name.'''
        ...
    
    def get_json_str_by_uid(self, uid : str, filename : str) -> str:
        '''Gets the JSON  string  of the file from the cache using the specified unique id,set the output filename in the JSON.
        
        :param uid: The unique id for the file cache.
        :param filename: Specifies the file name in the JSON. If set to null,the default filename is: book1.
        :returns: The JSON  string'''
        ...
    
    def lazy_loading_json_str(self, uid : str, sheet_name : str) -> str:
        ...
    
    @staticmethod
    def get_uid_for_file(file_name : str) -> str:
        '''Generates a new unique id for the file cache using the given file name.
        
        :param file_name: The file name.'''
        ...
    
    def import_excel_file_from_json(self, json : str):
        '''Imports the excel file from JSON format string.
        
        :param json: The JSON format string.'''
        ...
    
    def merge_excel_file_from_json(self, uid : str, json : str):
        '''Applies a batch update to the memory data.
        
        :param uid: The unique id for the file cache.
        :param json: The update JSON format string.'''
        ...
    
    def save_to_cache_with_file_name(self, uid : str, filename : str, password : str):
        '''Saves the memory data to the cache file with the specified filename and also set the open password, the save format is baseed on the file extension of the filename  .
        
        :param uid: The unique id for the file cache.
        :param filename: The filename to save.
        :param password: The excel file's open password. The value can be null If no passowrd is set.'''
        ...
    
    @staticmethod
    def get_image_stream(uid : strpicid : str) -> io.RawIOBase:
        '''Get Stream of image.
        
        :param uid: The unique id for the file cache.
        :param picid: The image id.
        :returns: The image stream'''
        ...
    
    def get_ole(self, uid : str, sheetname : str, oleid : int, label : Any) -> bytes:
        '''Gets the byte array data of the  embedded ole object .
        
        :param uid: The unique id for the file cache.
        :param sheetname: The worksheet name.
        :param oleid: The  id for the embedded ole object.
        :param label: The display label of the embedded ole object.
        :returns: The byte array data of the  embedded ole object .'''
        ...
    
    def check_in_cache_for_collaborative(self, uid : str) -> bool:
        '''Check wether workbook instance is in memory cache .this method is apply for Collaborative mode only.'''
        ...
    
    def update_cell(self, p : str, uid : str) -> str:
        '''Applies the update operation.
        
        :param p: The JSON format string of update operation.
        :param uid: The unique id for the file cache.
        :returns: The JSON format string of the update result.'''
        ...
    
    def insert_image(self, uid : str, p : str, s : io.RawIOBase, image_url : str) -> str:
        '''Inserts image in the worksheet from file stream or the URL,(either the file stream or the URL shall be provided)
        or
        Inserts shape ,when the p.type is one of AutoShapeType
        
        :param uid: The unique id for the file cache
        :param p: The JSON format string for the operation which specify the cell location  ,the worksheet name,upper left row,upper left column for the image，etc  {name:'sheet1',ri:1,ci:1}
        :param s: The file stream of the image file
        :param image_url: The URL of the image file
        :returns: The JSON format string of the inserted image'''
        ...
    
    def copy_image_or_shape(self, uid : str, p : str) -> str:
        '''Copys image or shape.
        
        :param uid: The unique id for the file cache.
        :param p: The JSON string for the operation which specify the cell location ,it contains the worksheet name,upper left row,upper left column for the image or shape，etc  {name:'sheet1',ri:1,ci:1,srcid:2,srcname:'sheet2',isshape:true}
        :returns: The JSON string of the new copied image'''
        ...
    
    def error_json(self, msg : str) -> str:
        '''Gets the error message string in JSON format.
        
        :param msg: The error message.
        :returns: The JSON string.'''
        ...
    
    @staticmethod
    def get_grid_load_format(extension : str) -> aspose.cellsgridjs.GridLoadFormat:
        '''Gets the load format by file extension
        
        :param extension: The file extention ,usually start with '.' .'''
        ...
    
    @staticmethod
    def get_image_url(uid : strpicid : str, delimiter : str) -> str:
        '''Gets the image URL.
        
        :param uid: The unique id for the file cache.
        :param picid: The image id.
        :param delimiter: The string delimiter.'''
        ...
    
    @staticmethod
    def set_image_url_base(base_image_url : str):
        '''Set the base image get action URL from controller .
        
        :param base_image_url: the base image get action URL.'''
        ...
    
    @property
    def settings(self) -> aspose.cellsgridjs.GridWorkbookSettings:
        '''Represents the workbook settings.'''
        ...
    
    @settings.setter
    def settings(self, value : aspose.cellsgridjs.GridWorkbookSettings):
        '''Represents the workbook settings.'''
        ...
    
    @classmethod
    @property
    def cache_imp(cls) -> aspose.cellsgridjs.GridCacheForStream:
        ...
    
    @classmethod
    @cache_imp.setter
    def cache_imp(cls, value : aspose.cellsgridjs.GridCacheForStream):
        ...
    
    @classmethod
    @property
    def calculate_engine(cls) -> aspose.cellsgridjs.GridAbstractCalculationEngine:
        ...
    
    @classmethod
    @calculate_engine.setter
    def calculate_engine(cls, value : aspose.cellsgridjs.GridAbstractCalculationEngine):
        ...
    
    @classmethod
    @property
    def update_monitor(cls) -> aspose.cellsgridjs.GridUpdateMonitor:
        ...
    
    @classmethod
    @update_monitor.setter
    def update_monitor(cls, value : aspose.cellsgridjs.GridUpdateMonitor):
        ...
    
    ...

class GridReferredArea:
    '''Represents a referred area by the formula.'''
    
    def get_values(self) -> any:
        '''Gets cell values in this area.
        
        :returns: If this area is invalid, "#REF!" will be returned;
        If this area is one single cell, then return the cell value object;
        Otherwise return one array for all values in this area.'''
        ...
    
    def get_value(self, row_offset : int, col_offset : int) -> any:
        '''Gets cell value with given offset from the top-left of this area.
        
        :param row_offset: row offset from the start row of this area
        :param col_offset: column offset from the start row of this area
        :returns: "#REF!" if this area is invalid;
        "#N/A" if given offset out of this area;
        Otherwise return the cell value at given position.'''
        ...
    
    @property
    def is_external_link(self) -> bool:
        ...
    
    @property
    def external_file_name(self) -> str:
        ...
    
    @property
    def sheet_name(self) -> str:
        ...
    
    @property
    def is_area(self) -> bool:
        ...
    
    @property
    def end_column(self) -> int:
        ...
    
    @property
    def start_column(self) -> int:
        ...
    
    @property
    def end_row(self) -> int:
        ...
    
    @property
    def start_row(self) -> int:
        ...
    
    ...

class GridUpdateMonitor:
    '''Monitor for user to track the change of update operation.'''
    
    def after_update(self, op : str, uid : str, cells : list):
        '''after update operation
        
        :param op: The JSON string for update operation
        :param uid: The unique id for the file cache.
        :param cells: The Updated Cells list,include cells which has style change,value change or formula change'''
        ...
    
    ...

class GridWorkbookSettings:
    '''Represents the settings of the workbook.'''
    
    @property
    def max_iteration(self) -> int:
        ...
    
    @max_iteration.setter
    def max_iteration(self, value : int):
        ...
    
    @property
    def iteration(self) -> bool:
        '''Indicates whether use iteration to resolve circular references.'''
        ...
    
    @iteration.setter
    def iteration(self, value : bool):
        '''Indicates whether use iteration to resolve circular references.'''
        ...
    
    @property
    def force_full_calculate(self) -> bool:
        ...
    
    @force_full_calculate.setter
    def force_full_calculate(self, value : bool):
        ...
    
    @property
    def create_calc_chain(self) -> bool:
        ...
    
    @create_calc_chain.setter
    def create_calc_chain(self, value : bool):
        ...
    
    @property
    def re_calculate_on_open(self) -> bool:
        ...
    
    @re_calculate_on_open.setter
    def re_calculate_on_open(self, value : bool):
        ...
    
    @property
    def precision_as_displayed(self) -> bool:
        ...
    
    @precision_as_displayed.setter
    def precision_as_displayed(self, value : bool):
        ...
    
    @property
    def date1904(self) -> bool:
        '''Gets a value which represents if the workbook uses the 1904 date system.'''
        ...
    
    @date1904.setter
    def date1904(self, value : bool):
        '''Sets a value which represents if the workbook uses the 1904 date system.'''
        ...
    
    @property
    def enable_macros(self) -> bool:
        ...
    
    @enable_macros.setter
    def enable_macros(self, value : bool):
        ...
    
    @property
    def check_custom_number_format(self) -> bool:
        ...
    
    @check_custom_number_format.setter
    def check_custom_number_format(self, value : bool):
        ...
    
    @property
    def author(self) -> str:
        '''Gets/sets the author of the file.'''
        ...
    
    @author.setter
    def author(self, value : str):
        '''Gets/sets the author of the file.'''
        ...
    
    ...

class IGridJsService:
    '''Reprensents the basic operation apis interface used in controller actions.'''
    
    def update_cell(self, p : str, uid : str) -> str:
        '''Applies the update operation.
        
        :param p: The JSON format string of update operation.
        :param uid: The unique id for the file cache.
        :returns: The JSON format string of the update result.'''
        ...
    
    def check_in_cache_for_collaborative(self, uid : str) -> bool:
        '''Check wether workbook instance is in memory cache .this method is apply for Collaborative mode only.'''
        ...
    
    def detail_stream_json_with_uid(self, stream : io.RawIOBase, file_path : str, uid : str):
        '''Write the JSON string  for the file to the stream  by the specified unique id.
        
        :param stream: The stream that will be written
        :param file_path: The file path
        :param uid: The unique id for the file cache.'''
        ...
    
    def detail_stream_json(self, stream : io.RawIOBase, file_path : str):
        '''Write the JSON string  for the Workbook to the stream
        
        :param stream: The stream that will be written
        :param file_path: The file path'''
        ...
    
    def lazy_loading_stream_json(self, stream : io.RawIOBase, sheet_name : str, uid : str):
        '''Writes the JSON string of the specified sheet in the file from the cache using the specified unique id  to the stream..
        
        :param stream: The stream that will be written
        :param sheet_name: The sheet name.
        :param uid: The unique id for the file cache.'''
        ...
    
    def add_image_by_url(self, p : str, uid : str, imageurl : str) -> str:
        ...
    
    def copy_image(self, p : str, uid : str) -> str:
        '''Applies the copy image operation.
        
        :param p: The JSON string parameter
        :param uid: The unique id for the file cache.
        :returns: The JSON string result'''
        ...
    
    def load(self, uid : str, filename : str) -> str:
        '''Gets the JSON  string  of the file from the cache using the specified unique id,set the output filename in the JSON.
        
        :param uid: The unique id for the file cache.
        :param filename: Specifies the file name in the JSON. If set to null,the default filename is: book1.
        :returns: The JSON string'''
        ...
    
    def image(self, uid : str, picid : str) -> io.RawIOBase:
        '''Get Stream of image.
        
        :param uid: The unique id for the file cache.
        :param picid: The image id.
        :returns: The image stream'''
        ...
    
    def ole(self, uid : str, sheetname : str, oleid : int, label : Any) -> bytes:
        '''Gets the byte array data of the  embedded ole object .
        
        :param uid: The unique id for the file cache.
        :param sheetname: The worksheet name.
        :param oleid: The  id for the embedded ole object.
        :param label: The display label of the embedded ole object.
        :returns: The byte array data of the  embedded ole object .'''
        ...
    
    def image_url(self, base_url : str, picid : str, uid : str) -> str:
        '''Gets the image URL.
        
        :param base_url: The base action URL.
        :param picid: The image id.
        :param uid: The unique id for the file cache.
        :returns: The image URL'''
        ...
    
    def get_file(self, fileid : str) -> io.RawIOBase:
        '''Get file stream
        
        :param fileid: the file id
        :returns: The stream of the file'''
        ...
    
    def download(self, p : str, uid : str, filename : str) -> str:
        '''Applies the download file operation
        
        :param p: The JSON parameter
        :param uid: The unique id for the file cache.
        :param filename: The file name
        :returns: The file URL'''
        ...
    
    ...

class GridExceptionType:
    '''Represents custom exception code for GridJs.'''
    
    @classmethod
    @property
    def CHART(cls) -> GridExceptionType:
        '''Invalid chart setting.'''
        ...
    
    @classmethod
    @property
    def DATA_TYPE(cls) -> GridExceptionType:
        '''Invalid data type setting.'''
        ...
    
    @classmethod
    @property
    def DATA_VALIDATION(cls) -> GridExceptionType:
        '''Invalid data validation setting.'''
        ...
    
    @classmethod
    @property
    def CONDITIONAL_FORMATTING(cls) -> GridExceptionType:
        '''Invalid data validation setting.'''
        ...
    
    @classmethod
    @property
    def FILE_FORMAT(cls) -> GridExceptionType:
        '''Invalid file format.'''
        ...
    
    @classmethod
    @property
    def FORMULA(cls) -> GridExceptionType:
        '''Invalid formula.'''
        ...
    
    @classmethod
    @property
    def INVALID_DATA(cls) -> GridExceptionType:
        '''Invalid data.'''
        ...
    
    @classmethod
    @property
    def INVALID_OPERATOR(cls) -> GridExceptionType:
        '''Invalid operator.'''
        ...
    
    @classmethod
    @property
    def INCORRECT_PASSWORD(cls) -> GridExceptionType:
        '''Incorrect password.'''
        ...
    
    @classmethod
    @property
    def LICENSE(cls) -> GridExceptionType:
        '''License related errors.'''
        ...
    
    @classmethod
    @property
    def LIMITATION(cls) -> GridExceptionType:
        '''Out of MS Excel limitation error.'''
        ...
    
    @classmethod
    @property
    def PAGE_SETUP(cls) -> GridExceptionType:
        '''Invalid page setup setting.'''
        ...
    
    @classmethod
    @property
    def PIVOT_TABLE(cls) -> GridExceptionType:
        '''Invalid pivotTable setting.'''
        ...
    
    @classmethod
    @property
    def SHAPE(cls) -> GridExceptionType:
        '''Invalid drawing object setting.'''
        ...
    
    @classmethod
    @property
    def SPARKLINE(cls) -> GridExceptionType:
        '''Invalid sparkline object setting.'''
        ...
    
    @classmethod
    @property
    def SHEET_NAME(cls) -> GridExceptionType:
        '''Invalid worksheet name.'''
        ...
    
    @classmethod
    @property
    def SHEET_TYPE(cls) -> GridExceptionType:
        '''Invalid worksheet type.'''
        ...
    
    @classmethod
    @property
    def INTERRUPTED(cls) -> GridExceptionType:
        '''The process is interrupted.'''
        ...
    
    @classmethod
    @property
    def IO(cls) -> GridExceptionType:
        '''The file is invalid.'''
        ...
    
    @classmethod
    @property
    def PERMISSION(cls) -> GridExceptionType:
        '''Permission is required to open this file.'''
        ...
    
    @classmethod
    @property
    def UNSUPPORTED_FEATURE(cls) -> GridExceptionType:
        '''Unsupported feature.'''
        ...
    
    @classmethod
    @property
    def UNSUPPORTED_STREAM(cls) -> GridExceptionType:
        '''Unsupported stream to be opened.'''
        ...
    
    @classmethod
    @property
    def UNDISCLOSED_INFORMATION(cls) -> GridExceptionType:
        '''Files contains some undisclosed information.'''
        ...
    
    ...

class GridLoadFormat:
    '''Represents the load file format.'''
    
    @classmethod
    @property
    def AUTO(cls) -> GridLoadFormat:
        '''Represents recognizing the format automatically.'''
        ...
    
    @classmethod
    @property
    def CSV(cls) -> GridLoadFormat:
        '''Represents Comma-Separated Values(CSV) text file.'''
        ...
    
    @classmethod
    @property
    def XLSX(cls) -> GridLoadFormat:
        '''Represents Office Open XML spreadsheetML workbook or template, with or without macros.'''
        ...
    
    @classmethod
    @property
    def TSV(cls) -> GridLoadFormat:
        '''Represents   TSV(tab-separated values file) file.'''
        ...
    
    @classmethod
    @property
    def TAB_DELIMITED(cls) -> GridLoadFormat:
        '''Represents  tab delimited text file, same with :py:attr:`aspose.cellsgridjs.GridLoadFormat.TSV`.'''
        ...
    
    @classmethod
    @property
    def HTML(cls) -> GridLoadFormat:
        '''Represents   html file.'''
        ...
    
    @classmethod
    @property
    def M_HTML(cls) -> GridLoadFormat:
        '''Represents   mhtml file.'''
        ...
    
    @classmethod
    @property
    def ODS(cls) -> GridLoadFormat:
        '''Represents  Open Document Sheet(ODS) file.'''
        ...
    
    @classmethod
    @property
    def EXCEL_97_TO_2003(cls) -> GridLoadFormat:
        '''Represents   Excel97-2003 xls file.'''
        ...
    
    @classmethod
    @property
    def SPREADSHEET_ML(cls) -> GridLoadFormat:
        '''Represents   Excel 2003 xml file.'''
        ...
    
    @classmethod
    @property
    def XLSB(cls) -> GridLoadFormat:
        '''Represents  xlsb file.'''
        ...
    
    @classmethod
    @property
    def NUMBERS(cls) -> GridLoadFormat:
        '''Represents  numbers file.'''
        ...
    
    @classmethod
    @property
    def FODS(cls) -> GridLoadFormat:
        '''Represents OpenDocument Flat XML Spreadsheet (.fods) file format.'''
        ...
    
    @classmethod
    @property
    def SXC(cls) -> GridLoadFormat:
        '''Represents StarOffice Calc Spreadsheet (.sxc) file format.'''
        ...
    
    @classmethod
    @property
    def UNKNOWN(cls) -> GridLoadFormat:
        '''Represents unrecognized format, cannot be loaded.'''
        ...
    
    ...

