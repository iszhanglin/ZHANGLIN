from cx_Freeze import setup, Executable
import encodings

setup(
    name='MyApp',
    version='1.0',
    description='My application',
    executables=[Executable('main1_pane.py')],
    options={
        'build_exe': {
            'packages': ['encodings'], 'include_files': []}})
