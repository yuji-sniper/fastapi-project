import glob
import zipfile

# with zipfile.ZipFile('test.zip', 'w') as z:
#     for f in glob.glob('test_dir/**', recursive=True):
#         z.write(f)

with zipfile.ZipFile('test.zip', 'r') as z:
    # z.extractall('zzz')
    with z.open('test_dir/test.txt') as f:
        print(f.read())
