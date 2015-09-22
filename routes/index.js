var express = require('express');
var router = express.Router();
var multiparty = require('multiparty');
var util = require('util');
var log4js = require('log4js');
var fs = require('fs');
var path = require('path');

// Mkdir logs
if (!fs.existsSync('logs')) {
	fs.mkdirSync('logs');
}
// Mkdir Files.
if (!fs.existsSync('public/files')) {
	fs.mkdirSync('public/files');
}
// Log Configure.
log4js.configure({
	appenders: [
		{ type: 'console' }, //控制台输出
		{
			type: 'file', //文件输出
			filename: 'logs/ip_access.log',
			maxLogSize: 1024,
			backups:3,
			category: 'ip'
		},
		{
			type: 'file', //文件输出
			filename: 'logs/result.log',
			maxLogSize: 1024,
			backups:3,
			category: 'res'
		},
		{
			type: 'file', //文件输出
			filename: 'logs/app.log',
			maxLogSize: 1024,
			backups:3,
			category: 'app'
		}
	]
});

ip_log = log4js.getLogger("ip");
res_log = log4js.getLogger("res");
/* App Name Mapping */
app_log = log4js.getLogger("app");

/* Get IP */
function getClientIp(req) {
	return req.headers['x-forwarded-for'] ||
		req.connection.remoteAddress ||
		req.socket.remoteAddress ||
		req.connection.socket.remoteAddress;
};

/* GET home page. */
router.get('/', function(req, res, next) {
	ip_log.trace(getClientIp(req));
	res.render('web', { title: 'LibRadar' });
});

router.get('/express', function(req, res, next) {
	res.render('index', { title: 'Express'});
})

router.get('/features', function(req, res, next) {
	res.render('features', {title: 'Features'});
})

router.get('/top_libs', function(req, res, next) {
	res.render('top_libs', {title: 'Top Libs'});
})

router.get('/contact', function(req, res, next) {
	res.render('contact', {title: 'Contact'});
})

router.get('/upload', function(req, res, next) {
	res.render('upload', { title: 'Upload' });
});

router.get('/radar', function(req, res, next) {
	res.render('web', {title: 'LibRadar'});
})

/*上传处理*/
router.post('/file/uploading', function(req, res, next){
	ip_log.warn(getClientIp(req));
  //生成multiparty对象，并配置下载目标路径
  res_log.warn(getClientIp(req));
  var form = new multiparty.Form({uploadDir: './public/files/'});
  //下载后处理
  form.parse(req, function(err, fields, files) {
    var filesTmp = JSON.stringify(files, null, 2);
    var file_original_name = "";
    if(err){
      console.log('parse error: ' + err);
    } else {
      var inputFile = files.inputFile[0];
      var uploadedPath = inputFile.path;
	  file_original_name = inputFile.originalFilename;
	  app_log.warn(uploadedPath + "," + getClientIp(req) + "," + file_original_name);
    }
	
	var exec = require('child_process').exec;
	//console.log(__dirname)

	pcwd = process.cwd()
	  // !!Importanct replace '/Users/marchon/Projects/PycharmProjects' with pcwd
	var cmdStr = 'python '+ '/Users/marchon/Projects/PycharmProjects' +'/LibRadar/main/detect.py ' + pcwd + '/' + uploadedPath;
	  console.log(cmdStr);
	exec(cmdStr, function(err, stdout, stderr){
		if (err) {
			console.log('Error' + cmdStr);
			res.render('result', {title: 'Error Occurred', libs: 'None', raw: stderr});
		} else {
			res_log.info(stdout);
			var sp = stdout.split('--Splitter--');
			var apktool = sp[0];
			var libs = sp[1];
			var liblist = [];
			/*
			if(libs.trim() != "") {
				//console.log(JSON.parse(libs));
				liblist = JSON.parse(libs);
			}*/
			var routes = sp[2];
			/*
			if(routes.trim() == "") {
				routes = "";
			} else {
				routes = JSON.parse(routes);
			}*/
			var time_consuming = sp[3];
			res.render('result', {title: 'LibRadar Result', original_name: file_original_name, apktool: apktool, libs: libs , routes: routes, time_c: time_consuming, raw: stdout});
		}
	});
	
	
 });
});


module.exports = router;
