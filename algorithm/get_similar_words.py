#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:LL
# 2020

# 问题描述：对于一个文本集合，把相似的单词进行归类。这里这样定义相似单词：两个单词只有一个字母不一样!
# 方法一：对于这个问题，我们最开始使用的是暴力穷举办法。遍历文本中的每个单词，找出在文本中与其相似的单词，
# 算法的时间复杂度是o(n2),
# 对于常见的英文词典，差不多有将近20000万个单词，那么需要经过4亿次运算，时间惊人，在实际中不可能行得通。
# 当然这里还是有一个trick，因为相似单词总是长度一样的，所以你也许可以少许多计算。（当然这不能从根本上改变大局）

# 方法二： 从相似单词的特点入手。‘son’和‘sun’都可以用正则表达式中的‘s.n’来表示，其中.在正则表达式中可以代表任意的符号
# 我们使用一个一个字典结构：key是正则字符串 value：是相似单词的集合。举个例子：对于单词'son',那么符合它的正则匹配有
# ‘.on’,'s.n','so.',那么字典中，分别是：key:'.on',value:'son',key:'s.n',value:'son',key:'so.',value:'son'，对于单词‘sun’,
# 进行同样的计算，同时字典开始更新：key:'.un',value:'sun',key:'s.n',value:['son','sun'],key:'so.',value:'son'
# key:'su.',value:'sun'。这样遍历文本，最后的时间复杂度是o(n):


