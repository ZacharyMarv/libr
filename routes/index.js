var express = require('express');
var router = express.Router();
var log4js = require('log4js');
var fs = require('fs');

// Mkdir logs
if (!fs.existsSync('logs')) {
	fs.mkdirSync('logs');
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
	res.render('web5', { title: 'LibRadar' });
});

router.get('/h4', function(req, res, next) {
	res.render('web', { title: 'LibRadar_HTML4'});
});

router.get('/express', function(req, res, next) {
	res.render('index', { title: 'Express'});
})

router.get('/features', function(req, res, next) {
	res.render('features', {title: 'Features'});
})

router.get('/top_libs', function(req, res, next) {
	fs.readFile('public/data/top_libs.json',{encoding:'utf-8'},function(err, data) {
		if (err) {
			console.log(err);
			res.render('error', {title: 'Top Libs Error', err: err});
		} else {
			// console.log(data);
			res.render('top_libs', {title: 'Top Libs', top_libs: data});
		}
	});
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


module.exports = router;
