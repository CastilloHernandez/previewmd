import os
import mimetypes
import hashlib

def BuscarImagenes(dir):
	r=[]
	for root, dirs, files in os.walk(dir):
		#print root
		for file in files:	
			if str(mimetypes.guess_type(file)[0]).split('/')[0] == 'image':
				r.append(str(os.path.join(root,file)).split('trunk')[1])
	return sorted(r)	
def BuscarReadmes(dir):
	r=[]
	for root, dirs, files in os.walk(dir):
		#print root
		for file in files:
			#print file
			if file == 'README.md':
				r.append(root)
	return sorted(r)
	
for d in BuscarReadmes('.'):
	#print d
	c=[]
	o=''
	HashOriginal=''
	HashModificado=''
	NecesitaLineaEnBlanco=False
	AgregarContenido=False
	ImagenesAgregadas=False
	#print 'Analizando: ' + os.path.join(d,'README.md')
	with open(os.path.join(d,'README.md'),'r') as f:
		o=f.read().replace('\r\n','\n')
		HashOriginal=hashlib.md5(o).hexdigest()
		for l in o.splitlines():
			if l.startswith('## Contenido'):
				AgregarContenido=True
				break
			if not l.startswith('---'):
				if not l.startswith('!['):
					c.append(l + '\n')
		while len(c[-1])<=1:
			c.pop()
		if len(c[-1])>1:
			NecesitaLineaEnBlanco=True
	if AgregarContenido:
		if NecesitaLineaEnBlanco:
			NecesitaLineaEnBlanco=False
			c.append('\n')
		c.append('## Contenido\n')
		for r in BuscarReadmes(d):
			if not r == d:
				with open(os.path.join(r,'README.md'),'r') as f:
					for l in f.read().splitlines():
						if l.startswith('# '):
							c.append('* ' + l[2:] + '\n')
						if l.startswith('##'):
							c.append('\t*' + l[2:] + '\n')
						if l.startswith('* '):
							c.append('\t\t* ' + l[2:] + '\n')
	if len(c[-1])>1:
		NecesitaLineaEnBlanco=True
	for i in BuscarImagenes(d):
		ImagenesAgregadas=True
		if NecesitaLineaEnBlanco:
			NecesitaLineaEnBlanco=False
			c.append('\n')
		c.append('---\n')
		c.append('![' + os.path.basename(i) + '](' + i.replace(chr(92),chr(47)) + ')\n')
	if ImagenesAgregadas:
		c.append('---\n')
	HashModificado=hashlib.md5(''.join(c)).hexdigest()
	if HashOriginal==HashModificado:
		print 'Sin cambios: ' + os.path.join(d,'README.md')
	else:
		print 'Modificado: ' + os.path.join(d,'README.md')
		with open(os.path.join(d,'README.md'),'wb') as f:
			f.writelines(c)

	#print BuscarImagenes(d)
