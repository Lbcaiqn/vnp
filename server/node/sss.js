const express=require('express')
let bodyParser = require('body-parser')
let fs=require('fs')
let path = require("path")
const exec = require('child_process').exec
const multer = require("multer")
const { RSA_PKCS1_OAEP_PADDING } = require('constants')
const { content } = require('./data/ShowContent.js')



const app=express()
app.use(express.static('./public'))

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))



/*路由----------------------------------------------------------------------*/

app.all("*", (req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  next();
})

app.all('/aaa',(request,response,next)=>{ 
  response.setHeader("Access-Control-Allow-Headers","content-type");
  response.setHeader("Access-Control-Allow-Methods","DELETE,PUT,POST,GET,OPTIONS");
  if (request.method == 'OPTIONS')  response.send(200);  //让options尝试请求快速结束
  else{
    let r=request.body.submitData,fn=request.body.fn
    //删除文件
    let files=[],path='./public/DrawImg'
    files = fs.readdirSync(path);
    // files.forEach((file, index) => {
    //   let curPath = path + "/" + file;
    //   fs.unlinkSync(curPath)
    // })
    
    fs.writeFile(`../py/${fn}.json`,JSON.stringify(r),{encoding: 'utf8'},(err)=>{
      exec('python3 ../py/1.py '+fn,(error,stdout,stderr) => {
        if(error) {
            console.info('pyrhon报错啦'+stderr)
            response.send('#')
            
            return next(err)
            
        }
        console.log(stdout)
        fs.stat(`./public/DrawImg/${fn}.jpg`,(err,data)=>{
          if(err) response.send('#')
          else  response.send(`http://47.107.225.248:8000/DrawImg/${fn}.jpg?`+new Date().valueOf())
        })
      
      })
    })
  
  
  }
})

// 文件上传
app.post("/upload", multer({ dest: "../py/csv" }).any(), (req, res) => {
  //文件已经上传到 '../py/ 下'，现在需要对文件重命名
  //解构出文件名和后缀名
  const { fieldname, originalname } = req.files[0];
  //取出文件名
  const name = fieldname.slice(0, fieldname.indexOf("."));
  //路径+文件名+后缀名
  const newName ='../py/csv/' + name + path.parse(originalname).ext;
  //开始重命名
  fs.rename(req.files[0].path, newName, (err) => {
    if(err) res.send("上传失败")
    else    res.send(newName)
  })
})

//返回数据
app.get('/show',(request,response) => {
  response.send(content)
})


app.listen(8000,()=>[
  console.log('服务已启动') 
])








