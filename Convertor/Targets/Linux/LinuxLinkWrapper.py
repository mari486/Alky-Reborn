# Copyright 2006 Falling Leaf Systems, LLC.
# Refer to LICENSE in the root directory.

import os

class LinuxLinkWrapper:
	def __init__(self, source, shared):
		self.source      = source
		self.shared      = shared
		self.imports     = source.imports
		self.entry_point = source.entry_point
	
	def output(self, filename):
		linkwrapper = file('Targets/Linux/linkwrapper.c', 'r').read()
		linkwrapper = linkwrapper.replace('%IMPORT_PATH%', '/tmp/imports.h')
		linkwrapper = linkwrapper.replace('%ENTRY_POINT%', '0x%08x' % self.entry_point)
		
		shared = []
		for obj in self.shared:
			name, image_base, entry_point = obj
			shared.append('SHARED(%s, %08x, 0x%08x);' % (name, image_base, entry_point))
		
		linkwrapper = linkwrapper.replace('%SHARED%', '\n'.join(shared))
		
		fp = file('/tmp/linkwrapper.c', 'w')
		fp.write(linkwrapper)
		fp.close()
		
		fp = file('/tmp/imports.h', 'w')
		
		for imp in self.imports:
			imp = self.imports[imp]
			print >>fp, 'IMPORT("%s", "%s", 0x%08x);' % (imp[1].lower().replace('.dll', ''), imp[2], imp[3])
		
		fp.close()
		
		ret = os.system('gcc -c -pie -o %s %s -I../LibAlky' % (filename, '/tmp/linkwrapper.c'))
		
		if ret != 0:
			return False
		
		return True
