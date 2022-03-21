export const mid2behind=function(zhong){
  let hou=''   //后缀表达式
  let stack=[] //辅助栈
  //定义优先级
  const priority={
    '+':1,
    '-':1,
    '*':2,
    '/':2
  }
  //1、遍历中缀表达式
  for(let i of zhong){
    //1.1 如果是数字，不管位数，直接入栈
    if(i >= '0' && i <= '9' || i == 'c' || i == '.') hou+=i 
    //1.2 非数字
    else{
      //1.2.1 +=*/
      if(i == '+' || i == '-' || i == '*' || i == '/'){
        //加上空格，区分每个数字
        hou += ' '
        //若栈空或栈顶为'('或i优先级高于栈顶元素，i入栈
        if(stack.length == 0 || stack[stack.length-1] == '(' || priority[i] > priority[stack[stack.length-1]])  stack.push(i)
        //否则，依次出栈加入后缀表达式，直到'('或优先级高于栈顶
        else{
          while(true){
            if(stack.length == 0 || stack[stack.length-1] == '(' || priority[i] > priority[stack[stack.length-1]]){
              stack.push(i)
              break
            }
            hou += stack.pop() + ' '
         }
       }
      }
      //1.2.2 (
      else if(i == '(') stack.push(i)
      //1.2.3 )
      else if(i == ')'){
        //依次出栈加入后缀表达式，直到'(',删除'('
        while(true){
          if(stack[stack.length-1] == '('){
            stack.pop()
            break
          }
          hou += ' ' + stack.pop()
        }
      }
    }
  }
  //2、遍历完成，若栈非空，依次出栈加入到后缀表达式，直到栈空
  while(stack.length != 0){
    hou += ' ' + stack.pop()
    
  }
  return hou
}
