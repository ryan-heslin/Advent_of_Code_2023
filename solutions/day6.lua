local parse = function(path)
    local out = {}
    for line in io.lines(path) do
        local key = string.lower(string.match(line, "^%a+"))
        local result = {}
        for match in string.gmatch(line, "(%d+)") do
            table.insert(result, tonumber(match))
        end
        out[key] = result
    end
    return out
end

local quadratic = function(a, b, c)
    local discrim = math.sqrt((b ^ 2) - (4 * a * c))
    local denom = 2 * a
    return { (-b + discrim) / denom, (-b - discrim) / denom }
end

local intercepts = function(time, dist)
    return quadratic(-1, time, -dist)
end

local num_bool = function(e)
    return (e and 1) or 0
end

local solve = function(data)
    local result = 1
    for i, _ in ipairs(data.time) do
        local points = intercepts(data.time[i], data.distance[i])
        -- Need to handle case where intercepts are integers and therefore invalid
        local left_i = math.min(points[1], points[2])
        local left = math.max(1, math.ceil(left_i + num_bool(left_i % 1 == 0)))
        local right_i = math.max(points[1], points[2])
        local right = math.min(
            math.floor(right_i - num_bool(right_i % 1 == 0)),
            data.time[i] - 1
        )
        result = result * (right - left + 1)
    end
    return result
end

concat_numbers = function(nums)
    local result = ""
    for _, el in ipairs(nums) do
        result = result .. tostring(el)
    end
    return tonumber(result)
end

local raw = parse("inputs/day6.txt")
local part1 = solve(raw)
print(part1)

local combined = {}
for key, el in pairs(raw) do
    print(el == nil)
    combined[key] = { concat_numbers(el) }
end
local part2 = solve(combined)
print(part2)
