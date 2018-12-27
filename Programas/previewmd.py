import os
import mimetypes
import hashlib
import urllib2
import argparse

def get_redirected_url(url):
	opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
	request = opener.open(url)
	return request.url

def BuscarImagenes(dir):
	r=[]
	for root, dirs, files in os.walk(dir):
		for file in files:
			if str(mimetypes.guess_type(file)[0]).split('/')[0] == 'image':
				r.append('/'+ '/'.join(str(os.path.join(root,file)).replace(chr(92),chr(47)).split('/')[1:]))
	return sorted(r)
def BuscarReadmes(dir):
	r=[]
	for root, dirs, files in os.walk(dir):
		for file in files:
			if file == 'README.md':
				r.append(root)
	return sorted(r)

parser = argparse.ArgumentParser(prog='previewmd')
parser.add_argument('directorio',nargs='*')
opt = parser.parse_args()

directorios=[]
if len(opt.directorio):
	directorios=opt.directorio
else:
	directorios.append('.')

for directorio in directorios:
	for d in BuscarReadmes(directorio):
		c=[]
		o=''
		UrlAvatar=''
		HashOriginal=''
		HashModificado=''
		Seccion=''
		NecesitaLineaEnBlanco=False
		AgregarContenido=False
		ImagenesAgregadas=False
		with open(os.path.join(d,'README.md'),'r') as f:
			o=f.read().replace('\r\n','\n')
			HashOriginal=hashlib.md5(o).hexdigest()
			for l in o.splitlines():
				if l.startswith('## '):
					Seccion=l[3:]
				if l.startswith('## Contenido'):
					AgregarContenido=True
					break
				if not l.startswith('---'):
					if not l.startswith('!['):
						if l.startswith('* '):
							if l[2:].count(' ') == 0:
								if Seccion == 'Autores':
									try:
										print 'Buscando avatar de ' + l[2:]
										UrlAvatar=get_redirected_url('http://www.github.com/' + l[2:] + '.png')
										print 'Avatar encontrado ' + UrlAvatar
										c.append('* <a href="http://www.github.com/' + l[2:] + '">' + l[2:] + '</a> <img src="' + UrlAvatar + '" height="32" width="32">\n')	
									except:
										print 'Avatar no encontrado'
										c.append(l + '\n')
								else:
									c.append(l + '\n')
							else:
								c.append(l + '\n')
						else:
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
							if l.startswith('## '):
								c.append('\t* ' + l[3:] + '\n')
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
			c.append('![' + os.path.basename(i) + '](' + i.replace(chr(92),chr(47)).replace(' ','%20') + ')\n')
		if ImagenesAgregadas:
			c.append('---\n')
		HashModificado=hashlib.md5(''.join(c)).hexdigest()
		if HashOriginal==HashModificado:
			print 'Sin cambios: ' + os.path.join(d,'README.md')
		else:
			print 'Modificado: ' + os.path.join(d,'README.md')
			with open(os.path.join(d,'README.md'),'wb') as f:
				f.writelines(c)

