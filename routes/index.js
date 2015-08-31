var express = require('express');
var router = express.Router();
var multiparty = require('multiparty');
var util = require('util');
var fs = require('fs');
var path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('web', { title: 'Lib Radar' });
});

router.get('/express', function(req, res, next) {
	res.render('index', { title: 'Express'});
})

router.get('/features', function(req, res, next) {
	res.render('features', {title: 'Features'});
})

router.get('/contact', function(req, res, next) {
	res.render('contact', {title: 'Contact'});
})

router.get('/upload', function(req, res, next) {
	res.render('upload', { title: 'Upload' });
});

router.get('/radar', function(req, res, next) {
	res.render('web', {title: 'Lib Radar'});
})

/*上传处理*/
router.post('/file/uploading', function(req, res, next){
  //生成multiparty对象，并配置下载目标路径
  var form = new multiparty.Form({uploadDir: './public/files/'});
  //下载后处理
  form.parse(req, function(err, fields, files) {
    var filesTmp = JSON.stringify(files,null,2);
    var file_original_name = "";
    if(err){
      console.log('parse error: ' + err);
    } else {
      console.log('parse files: ' + filesTmp);
      var inputFile = files.inputFile[0];
      var uploadedPath = inputFile.path;
      var dstPath = './public/files/' + inputFile.originalFilename;
	  file_original_name = inputFile.originalFilename;
      //重命名为真实文件名
      fs.rename(uploadedPath, dstPath, function(err) {
        if(err){
          console.log('rename error: ' + err);
        } else {
          console.log('rename ok');
        }
      });
    }
	
	var exec = require('child_process').exec;
	//console.log(__dirname)
	var cmdStr = 'python /Users/marchon/Projects/NodeProjects/libr/lib-radar/get_b_hash/get_hash.py ' + path.join(__dirname,'.'+dstPath);
	exec(cmdStr, function(err, stdout, stderr){
		
		//console.log(cmdStr);
		if (err) {
			console.log('Error' + cmdStr);
			res.render('result', {title: 'Error Occurred', libs: 'None', raw: stderr});
		} else {
			var sp = stdout.split('--Spliter--');
			var apktool = sp[0];
			var libs = sp[1];
			if(libs.trim() == "") {
				libs = "None.";
			}
			var routes = sp[2];
			if(routes.trim() == "") {
				routes = "None.";
			}
			res.render('result', {title: 'Lib Radar Result', original_name: file_original_name, apktool: apktool, libs: libs , routes: routes, raw: stdout});
		}
		/*
	    res.writeHead(200, {'content-type': 'text/plain;charset=utf-8'});
	    res.write('received upload:\n');
		
		if (err) {
			console.log('Error' + cmdStr);
		}
		else {
			console.log('This is from Node.')
			var data = stdout;
			console.log(data);
			res.write(data);
		}
	
	    res.end(util.inspect({fields: fields, files: filesTmp}));*/
	});
	
	
 });
});


module.exports = router;
