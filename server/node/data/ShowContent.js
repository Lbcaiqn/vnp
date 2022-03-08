const url = 'http://localhost:8000/ShowImg/'

const content = {
  population:{
    dataDesc:{
      title: '数据说明',
      content:[
        {
          text: '111',
          img:[url+'population/data.png']
        }
      ]
    },
    scratter:{
      title: '散点图',
      content:[
        {text:'hahahahahahaha',img:['../../assets/img/a.png']},
        {text:'aaaa',img:['../../assets/img/0.png','../../assets/img/a.png']}
      ]
    },
    plot:{
      title: '折线图',
      content:[
        {text:'hahahahahahaha',img:['../../assets/img/a.png']},
        {text:'aaaa',img:['../../assets/img/0.png','../../assets/img/a.png']}
      ]
    }
  },
  temperature:{
    dataDesc: {
      title: '数据说明',
      content: [
        {text: '',img: [url+'temperature/data.png']}
      ]
    },
    scratter:{
      title: '散点图',
      content:[
        {text:'hahahahahahaha',img:['../../assets/img/a.png']},
        {text:'ccc',img:['../../assets/img/0.png','../../assets/img/a.png']}
      ]
    },
    plot:{
      title: '折线图',
      content:[
        {text:'hahahahahahaha',img:['../../assets/img/a.png']},
        {text:'aaaa',img:['../../assets/img/0.png','../../assets/img/a.png']}
      ]
    }
  }
}


module.exports = {
  content
}