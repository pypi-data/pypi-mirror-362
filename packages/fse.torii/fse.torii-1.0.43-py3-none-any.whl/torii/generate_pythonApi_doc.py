import validate
import pydoc
import os


api_file_src = '/opt/hpcg/core/bin/libhpcg/validate.py'
api_file_src_convert = os.path.realpath(api_file_src)

src_dir = os.path.dirname(os.path.realpath(__file__))
docs_dir = os.path.join(src_dir, 'docs')

if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)

os.chdir(docs_dir)
package = validate
# pydoc.writedocs(src_dir)
pydoc.writedoc('validate')

