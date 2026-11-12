from pathlib import Path
import base64,json,mimetypes,re,zipfile
p=Path(__file__).resolve().parent
def dataurl(path):
 f=p/path
 return 'data:'+(mimetypes.guess_type(str(f))[0] or 'application/octet-stream')+';base64,'+base64.b64encode(f.read_bytes()).decode()
css=(p/'styles.css').read_text()
css=re.sub(r"""url\(['"]?(assets/[^)'"]+)['"]?\)""",lambda m:"url('"+dataurl(m[1])+"')",css)
amap=(p/'asset-map.js').read_text()
amap=re.sub(r'"(assets/[^"]+)"',lambda m:json.dumps(dataurl(m[1])),amap)
app=(p/'app.js').read_text().replace('assets/hummingbird.png',dataurl('assets/hummingbird.png'))
html=(p/'index.html').read_text().replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>').replace('<script src="asset-map.js"></script>','<script>'+amap+'</script>').replace('<script src="app.js"></script>','<script>'+app+'</script>')
(p/'Business-Loans-PH.html').write_text(html)
with zipfile.ZipFile(p/'Business-Loans-PH-source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in ['index.html','styles.css','app.js','asset-map.js','README.md','verify.py','build.py']:
  z.write(p/name,'Business-Loans-PH/'+name)
 for f in (p/'assets').iterdir(): z.write(f,'Business-Loans-PH/assets/'+f.name)
print('Rebuilt standalone HTML and source archive.')
