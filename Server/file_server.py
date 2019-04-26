#import urllib3
#from urllib.parse import quote

from flask import Flask, make_response, request, session, render_template, send_file, Response,redirect
from flask.views import MethodView
from werkzeug import secure_filename
from datetime import datetime
import humanize
import os
import re
import stat
import json
import mimetypes
import shutil
#from config import config
app = Flask(__name__, static_url_path='/assets', static_folder='assets')
root = os.path.expanduser('/home/marcel/Desktop/OP1_File_Organizer/OP_1_Backup_Library')
path = ""#inside the backup folder



#root = os.path.expanduser('~')

ignored = ['^.bzr$', '^$RECYCLE.BIN$', '^.DAV$', '^.DS_Store$', '^.git$', '^.hg$', '^.htaccess$', '^.htpasswd$', '^.Spotlight-V100$',
           '^.svn$', '^__MACOSX$', '^ehthumbs.db$', '^robots.txt$', '^Thumbs.db$', '^thumbs.tps$']
datatypes = {'audio': 'm4a,mp3,oga,ogg,webma,wav, aif', 'archive': '7z,zip,rar,gz,tar',
             'image': 'gif,ico,jpe,jpeg,jpg,png,svg,webp', 'pdf': 'pdf', 'quicktime': '3g2,3gp,3gp2,3gpp,mov,qt',
             'source': 'atom,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml,plist',
             'text': 'txt', 'video': 'mp4,m4v,ogv,webm', 'website': 'htm,html,mhtm,mhtml,xhtm,xhtml'}
icontypes = {'fa-music': 'm4a,mp3,oga,ogg,webma,wav', 'fa-archive': '7z,zip,rar,gz,tar',
             'fa-picture-o': 'gif,ico,jpe,jpeg,jpg,png,svg,webp', 'fa-file-text': 'pdf',
             'fa-film': '3g2,3gp,3gp2,3gpp,mov,qt',
             'fa-code': 'atom,plist,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml',
             'fa-file-text-o': 'txt', 'fa-film': 'mp4,m4v,ogv,webm', 'fa-globe': 'htm,html,mhtm,mhtml,xhtm,xhtml'}



@app.route('/')
def base_redirect():
    return redirect("/index.html", code=302)

@app.route('/index.html')
def index(name=None):
    files = folders = []
    content = []
    for _, dirnames, filenames in os.walk(root+ "/"+path):
        folders = dirnames
        files = filenames
        break #TODO MAKE SIMPLER GOOD IF YOU WANT TO USE A TREE VIEW

    for f in folders:
        is_blacklisted = False
        for ig in ignored:
            if re.search(ig,str(f)):
                is_blacklisted = True
        if is_blacklisted:
            continue
        content.append({'type':'dir', 'name':f, 'mtime':os.stat(root+"/"+f).st_mtime})

    for f in files:
        is_blacklisted = False
        for ig in ignored:
            if re.search(ig, str(f)):
                is_blacklisted = True
        if is_blacklisted:
            continue
        content.append({'type':'file', 'name':f, 'mtime':os.stat(root+"/"+f).st_mtime,'size':os.stat(root+"/"+f).st_size})

    return render_template('index.html', name=name, path=path, total={'dir':len(folders),'file':len(files),'sum':len(files+folders)},contents=content)

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/", code=404)






@app.template_filter('size_fmt')
def size_fmt(size):
    try:
        tmp = int(size)
        return humanize.naturalsize(int(size))
    except NameError:
        return 0



@app.template_filter('time_fmt')
def time_desc(timestamp):
    mdate = datetime.fromtimestamp(timestamp)
    str = mdate.strftime('%Y-%m-%d %H:%M:%S')
    return str


@app.template_filter('data_fmt')
def data_fmt(filename):
    t = 'unknown'
    for type, exts in datatypes.items():
        if filename.split('.')[-1] in exts:
            t = type
    return t


@app.template_filter('icon_fmt')
def icon_fmt(filename):
    i = 'fa-file-o'
    for icon, exts in icontypes.items():
        if filename.split('.')[-1] in exts:
            i = icon
    return i


# /api/blocksdetected/getDebugImage/<usersession>
@app.route("/<path>/createFolder/<folderName>")
def createFolder(path, folderName):
    print(path, folderName)
    path = os.path.join(root, path)

    try:
        os.mkdir(path + "/" + folderName)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)
    return "Done"


@app.route("/deleteFolder/<folder_to_delete>")
def deleteFolder(folder_to_delete):
    #TODO ESCAPE STRING
    path = os.path.join(root, folder_to_delete)

    print path

    if not os.path.isdir(path):
        return json.dumps({'err': 'err','reason':'folder not exists or path is no folder'})#

    try:
        clear_folder(path)
        os.rmdir(path)

    except Exception as e:
        return json.dumps({'err': 'err','reason':e})

    return json.dumps({'err':'ok'})


@app.route("/deleteFile/<file_to_delete>")
def deleteFile(file_to_delete):
    path = os.path.join(root, file_to_delete)
    # TODO ESCAPE STRING
    print path

    if not os.path.isfile(path):
        return json.dumps({'err': 'err', 'reason': 'folder not exists or path is not a folder'})  #

    try:
        os.remove(path)
    except Exception as e:
        return json.dumps({'err': 'err', 'reason': e})

    return json.dumps({'err': 'ok'})


@app.template_filter('humanize')
def time_humanize(timestamp):
    mdate = datetime.utcfromtimestamp(timestamp)
    return humanize.naturaltime(mdate)


def get_type(mode):
    if stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
        type = 'dir'
    else:
        type = 'file'
    return type

def clear_folder(dir):
    if os.path.exists(dir):
        for the_file in os.listdir(dir):
            file_path = os.path.join(dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                else:
                    clear_folder(file_path)
                    os.rmdir(file_path)
            except Exception as e:
                print(e)


def partial_response(path, start, end=None):
    file_size = os.path.getsize(path)

    if end is None:
        end = file_size - start - 1
    end = min(end, file_size - 1)
    length = end - start + 1

    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    return response


def get_range(request):
    range = request.headers.get('Range')
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None


class PathView(MethodView):
    def get(self, p=''):
        hide_dotfile = request.args.get('hide-dotfile', request.cookies.get('hide-dotfile', 'no'))

        path = os.path.join(root, p)
        if os.path.isdir(path):
            contents = []
            total = {'size': 0, 'dir': 0, 'file': 0}
            for filename in os.listdir(path):
                if filename in ignored:
                    continue
                if hide_dotfile == 'yes' and filename[0] == '.':
                    continue
                filepath = os.path.join(path, filename)
                stat_res = os.stat(filepath)
                info = {}
                info['name'] = filename
                info['mtime'] = stat_res.st_mtime
                ft = get_type(stat_res.st_mode)
                info['type'] = ft
                total[ft] += 1
                sz = stat_res.st_size
                info['size'] = sz
                total['size'] += sz
                contents.append(info)
            page = render_template('index.html', path=p, contents=contents, total=total, hide_dotfile=hide_dotfile)
            res = make_response(page, 200)
            res.set_cookie('hide-dotfile', hide_dotfile, max_age=16070400)
        elif os.path.isfile(path):
            if 'Range' in request.headers:
                start, end = get_range(request)
                res = partial_response(path, start, end)
            else:
                res = send_file(path)
                res.headers.add('Content-Disposition', 'attachment')
        else:
            res = make_response('Not found', 404)
        return res

    # User Upload
    def post(self, p=''):
        path = os.path.join(root, p)
        info = {}
        if os.path.isdir(path):
            files = request.files.getlist('files[]')

            strBuilder = "UserUpload"
            if not os.path.isdir(path + "/" + strBuilder):
                os.makedirs(path + "/" + strBuilder)

            for file in files:
                try:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(path + "/" + strBuilder, filename)
                    file.save(filepath)
                except Exception as e:
                    info['status'] = 'error'
                    info['msg'] = str(e)
                else:
                    info['status'] = 'success'
                    info['msg'] = 'File Saved'
        else:
            info['status'] = 'error'
            info['msg'] = 'Invalid Operation'
        res = make_response(json.JSONEncoder().encode(info), 200)
        res.headers.add('Content-type', 'application/json')
        return res


path_view = PathView.as_view('path_view')
app.add_url_rule('/', view_func=path_view)
app.add_url_rule('/<path:p>', view_func=path_view)

app.run('0.0.0.0', 8000, threaded=True, debug=False)
