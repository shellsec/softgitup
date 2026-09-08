--[[
headinfo-begin
ScriptName=CppCommentTool
Desc=高亮或删除cpp注释
Author=psh
Version=1.0
Comment=该脚本可以高亮或删除当前编辑框中的cpp代码注释。
comboxPara1=颜色1高亮,颜色2高亮,颜色3高亮,清除高亮,删除注释,删除不含中文的注释
headinfo-end
]]

-- 功能索引 arg[1]（默认 0）：
--   0=颜色1高亮  1=颜色2高亮  2=颜色3高亮
--   3=清除高亮  4=删除注释  5=删除不含中文的注释
local mode = tonumber(arg[1]) or 0

local ed = ndd.editor()
if ed == nil then
    print("没有打开的编辑器")
    return
end

local editText = ed:get_text()

local Ranges = {}   -- 块注释范围 {start, finish}
local Ranges1 = {}  -- 单行注释范围 {start, finish}

local function clearHigh()
    ed:clear_all_high_light()
end

-- 判断字符串是否包含中文（UTF-8 中文字节首字节 E4~E9）
local function containsChinese(s)
    return string.find(s, "[\228-\233]") ~= nil
end

-- 判断 r 是否已被某个范围完全包含
local function isAlreadyInRange(r)
    for _, tempr in ipairs(Ranges) do
        if r.start >= tempr.start and r.finish <= tempr.finish then
            return true
        end
        if r.finish < tempr.start then
            return false
        end
    end
    return false
end

-- 单行注释是否合法：排除字符串字面量里的 //
-- pos / lineEndPos 为 1-based 字节索引
local function isSignalCommentValid(pos, lineEndPos)
    local start = pos - 1
    local times = 0
    while start >= 1 do
        local ch = editText:sub(start, start)
        if ch == "\n" then
            break
        elseif ch == '"' then
            times = times + 1
        end
        start = start - 1
    end

    -- 注释前有奇数个引号，且之后也有奇数个引号，说明 // 处于字符串中
    if times > 0 and times % 2 == 1 then
        times = 0
        local finish = pos
        while finish < lineEndPos do
            finish = finish + 1
            if editText:sub(finish, finish) == '"' then
                times = times + 1
            end
        end
        if times > 0 and times % 2 == 1 then
            return false
        end
    end
    return true
end

local function highLight(colorId)
    local times = 0   -- 块注释数
    local times1 = 0  -- 单行注释数

    -- 查找块注释 /* ... */（Lua pattern：.- 为非贪婪，. 匹配换行）
    local start = 1
    while true do
        local s, e = string.find(editText, "/%*.-%*/", start)
        if s == nil then break end
        local text = editText:sub(s, e)
        ed:high_light(s - 1, e - s + 1, colorId)
        if colorId ~= 5 then
            table.insert(Ranges, { start = s - 1, finish = e })
            times = times + 1
        elseif not containsChinese(text) then
            table.insert(Ranges, { start = s - 1, finish = e })
            times = times + 1
        end
        start = e + 1
    end

    -- 查找单行注释 //
    start = 1
    while true do
        local s, e = string.find(editText, "//[^\r\n]*", start)
        if s == nil then break end
        if isSignalCommentValid(s, e) then
            local text = editText:sub(s, e)
            local r = { start = s - 1, finish = e }
            ed:high_light(r.start, r.finish - r.start, colorId)
            if not isAlreadyInRange(r) then
                if colorId ~= 5 then
                    table.insert(Ranges1, r)
                    times1 = times1 + 1
                elseif not containsChinese(text) then
                    table.insert(Ranges1, r)
                    times1 = times1 + 1
                end
            end
        end
        start = e + 1
    end

    print(string.format("发现单行注释 %d 处", times1))
    print(string.format("发现多行注释 %d 处", times))

    -- 合并块注释到总范围
    for _, r in ipairs(Ranges) do
        table.insert(Ranges1, r)
    end

    -- 按 start 降序排序（从后往前删除，避免位置偏移）
    table.sort(Ranges1, function(a, b) return a.start > b.start end)

    -- 删除模式（colorId 4 或 5）
    if colorId == 4 or colorId == 5 then
        ed:begin_undo()
        for _, v in ipairs(Ranges1) do
            ed:delete_range(v.start, v.finish - v.start)
        end
        ed:end_undo()
    end
end

clearHigh()

if mode >= 0 and mode <= 2 then
    highLight(mode)
elseif mode == 3 then
    -- 仅清除高亮
elseif mode == 4 or mode == 5 then
    highLight(mode)
end

print("完成")
