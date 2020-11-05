# Class 3 【逆波兰式（后缀表达式）】

# 一 ) 中缀表达式
常见的表达式即为中缀表达式
## 例：A+B*(C-D)-E*F
![20140304145300156.jpg](https://cdn.nlark.com/yuque/0/2020/jpeg/2774814/1604540983884-9386f346-adf3-46b9-8960-5d7c5ff964ef.jpeg#align=left&display=inline&height=345&margin=%5Bobject%20Object%5D&name=20140304145300156.jpg&originHeight=345&originWidth=441&size=14649&status=done&style=none&width=441)
# 二）前缀表达式
上图前缀表达式：- + A * B - C D * E F
# 三）后缀表达式
上图后缀表达式：A B C D - * + E F * -
# 四）表达式计算

1. 中缀表达式转后缀表达式

思路整理：

- 准备一个队列存放最终结果（后缀表达式直接从左到右扫描进行计算即可）
- 准备一个栈存放操作符
- 为操作符设定优先级：
- 1）“(” 直接进栈（优先级最低），“)”弹栈，直到遇到左括号或者栈为空。
- 2）“+”“-”优先级低于“*”“/”。读入符号优先级高于栈顶符号，压栈；读入符号优先级低于栈顶符号，弹栈，直到遇到更低优先级符号或者“（”
- 3）最终将将栈中弹出，添加到队列中
```
public Queue<String> getRPN（表达式）{
	Queue<String> RPN = new LinkedList<>();
  Stack<String> op = new Stack<>();
  
  for(遍历表达式元素){
  	if（是数字）{
    	添加到RPN；
      continue}
    else{
    	if（左括号）{
      	添加到RPN；
        continue}
    	}
      if（右括号）{
      	while（op 非空 && op.peek() 非“(”）{
        	弹栈；
          添加到RPN；
        }
        // 弹出栈顶“(”
        op.pop()
        continue;
      }
     	if（新进入元素优先级大于栈顶元素）{
      	压栈
      }else{
      	while（op 非空 && op.peek() <= priority ）{
        	弹栈；
          添加到RPN；        
        }
					param压栈；
      }
    while（op 非空）{
    	弹栈；
      添加到RPN；
    }
  }
  返回后缀表达式RPN；
}
	 
```

2. 后缀表达式进行计算

思路整理：

- 准备一个栈放操作数
- 遍历队列，当遇到操作符，弹出两个操作数进行运算，并将结果压栈
```
public BigDecimal calculate（Queue<String> RPN）{
	Stack<Bigdecamal> num = new Stack<>();
	while(RPN 非空){
  	if（队首是数字）{
    	压栈
    }else{
    	弹出栈顶两个元素计算后压栈；
    }
  }
}
```


