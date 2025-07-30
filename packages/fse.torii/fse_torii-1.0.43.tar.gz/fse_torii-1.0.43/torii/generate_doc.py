import torii
import pydoc
import os
import pkgutil

src_dir = os.path.dirname(os.path.realpath(__file__))
docs_dir = os.path.join(src_dir, 'docs')

if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)

os.chdir(docs_dir)
package = torii
# pydoc.writedocs(src_dir)
pydoc.writedoc('torii')
for importer, modname, ispkg in pkgutil.walk_packages([src_dir], ''):
    if not modname.startswith('tests') and modname not in ['generate_doc', 'torii_main']:
        pydoc.writedoc('torii.' + modname)
