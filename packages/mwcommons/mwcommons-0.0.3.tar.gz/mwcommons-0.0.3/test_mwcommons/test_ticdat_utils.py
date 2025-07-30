import shutil
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from ticdat import PanDatFactory

from mwcommons.ticdat_utils import write_data


cwd = Path(__file__).parent.resolve()

# create a sample schema for testing
schema = PanDatFactory(sample_table=[['PK'], ['FloatCol', 'IntCol', 'TextCol', 'DateCol']])
schema.set_data_type(table='sample_table', field='PK', number_allowed=True, must_be_int=True, strings_allowed=())
schema.set_data_type(table='sample_table', field='FloatCol', number_allowed=True, must_be_int=False, strings_allowed=())
schema.set_data_type(table='sample_table', field='IntCol', number_allowed=True, must_be_int=True, strings_allowed=())
schema.set_data_type(table='sample_table', field='IntCol', number_allowed=False, strings_allowed='*')
schema.set_data_type(table='sample_table', field='DateCol', datetime=True)


class TestWriteData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # instantiate dat
        cls.dat = schema.PanDat()
        cls.dat.sample_table = pd.DataFrame({
            'PK': [1, 2, 3],
            'FloatCol': [1.1, 2.2, 3.3],
            'IntCol': [1, 2, 3],
            'TextCol': ['A', 'B', 'C'],
            'DateCol': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01'])
        })
        assert schema.good_pan_dat_object(cls.dat, bad_message_handler=print)
        
        # initialize temporary directory under cwd where tests will be performed
        cls.temp_root_dir = Path(tempfile.mkdtemp(prefix="test_write_data_", dir=cwd))
        
    @classmethod
    def tearDownClass(cls):
        # remove the temporary directory and all its contents
        if cls.temp_root_dir.exists() and cls.temp_root_dir.is_dir():
            shutil.rmtree(cls.temp_root_dir)

    def test_1_xlsx(self):
        """Saves data to xlsx under temp_root_dir"""
        output_path = self.temp_root_dir / "test_data.xlsx"
        write_data(sln=self.dat, output_data_loc=str(output_path), schema=schema)
        self.assertTrue(output_path.exists(), f"Output file {output_path} was not created")
        output_path.unlink()  # Clean up the created file after test
    
    def test_2_xlsx(self):
        """Saves data to xlsx under a subfolder of temp_root_dir that doesn't exist"""
        output_path = self.temp_root_dir / "subfolder" / "test_data.xlsx"
        with self.assertRaises(NotADirectoryError):
            write_data(sln=self.dat, output_data_loc=str(output_path), schema=schema)
    
    def test_3_json(self):
        """Saves data to json under temp_root_dir"""
        output_path = self.temp_root_dir / "test_data.json"
        write_data(sln=self.dat, output_data_loc=str(output_path), schema=schema)
        self.assertTrue(output_path.exists(), f"Output file {output_path} was not created")
        output_path.unlink()  # Clean up the created file after test
        
    def test_4_json(self):
        """Saves data to json under a subfolder of temp_root_dir that doesn't exist"""
        output_path = self.temp_root_dir / "subfolder" / "test_data.json"
        with self.assertRaises(NotADirectoryError):
            write_data(sln=self.dat, output_data_loc=str(output_path), schema=schema)
    
    def test_5_csv_directory(self):
        """Saves data to a csv file under temp_root_dir"""
        output_path = self.temp_root_dir
        output_file = output_path / "sample_table.csv"
        write_data(sln=self.dat, output_data_loc=str(output_path), schema=schema)
        self.assertTrue(output_file.exists(), f"Output file {output_file} was not created")
        output_file.unlink()  # Clean up the created file after test
    
    def test_6_csv_directory(self):
        """Saves data to a csv file under a subfolder temp_root_dir that doesn't exist yet"""
        output_path = self.temp_root_dir / "subfolder_that_does_not_exist"
        output_file = output_path / "sample_table.csv"
        write_data(sln=self.dat, output_data_loc=str(output_path), schema=schema)
        self.assertTrue(output_file.exists(), f"Output file {output_file} was not created")
        shutil.rmtree(output_path)  # Clean up the created directory after test
    
    def test_7_csv_directory(self):
        """Saves data to a csv file under a subsubfolder temp_root_dir that doesn't exist yet"""
        output_path = self.temp_root_dir / "folder_that_does_not_exist" / "subfolder_that_does_not_exist"
        with self.assertRaises(NotADirectoryError):
            write_data(sln=self.dat, output_data_loc=str(output_path), schema=schema)
        
    def test_8_csv_directory_with_extension(self):
        """Saves data to a csv file under a subfolder temp_root_dir with an extension, there should be a warning"""
        output_path = self.temp_root_dir / "subfolder_that_does_not_exist_2.extension"
        output_file = output_path / "sample_table.csv"
        
        msg = "output_data_loc's extension will be ignored and it'll be considered a directory instead"
        with self.assertWarnsRegex(UserWarning, msg):
            write_data(sln=self.dat, output_data_loc=str(output_path), schema=schema)

        self.assertTrue(output_file.exists(), f"Output file {output_file} was not created")
        shutil.rmtree(output_path)  # Clean up the created directory after test


if __name__ == "__main__":
    unittest.main(exit=False)
