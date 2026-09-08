--[[
headinfo-begin
ScriptName=Lua-text-Tool
Desc=基于lua提供对编辑框文本的操作
Author=psh
Version=1.0
Comment=该脚本可以对编辑框文本提供诸多快捷文本操作，比如删除行前空白，行自动缩进等。
comboxPara1=行前自动缩进4个空格,行前自动缩进2个制表符,行前自动缩进4个全角空白,去掉行前空白字符
headinfo-end
]]

-- 功能索引 arg[1]（默认 0）：
--   0=行前自动缩进4个空格  1=行前自动缩进2个制表符
--   2=行前自动缩进4个全角空白  3=去掉行前空白（含全角空白）
local mode = tonumber(arg[1]) or 0

local ed = ndd.editor()
if ed == nil then
    print("没有打开的编辑器")
    return
end

-- 全角空格 U+3000 的 UTF-8 字节
local FW = "\xE3\x80\x80"

-- 行首空白集合：tab、空格、全角空格
local leadBlank = "^[\t " .. FW .. "]*"

local replaceMap = {
    [0] = { leadBlank, "    " },
    [1] = { leadBlank, "\t\t" },
    [2] = { leadBlank, FW .. FW .. FW .. FW },
    [3] = { leadBlank, "" },
}

local item = replaceMap[mode]
if item == nil then
    print("未知的功能选项")
    return
end

-- mode=2 为正则模式；cs=1 区分大小写
local n = ed:replace(item[1], item[2], 2, 1)
print(string.format("替换了 %d 处", n))
