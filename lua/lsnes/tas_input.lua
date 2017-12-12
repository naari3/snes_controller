-- tas input
-- lsnes
-- only still 1P

filename = "example"

output, err = io.open(filename .. ".dat", "wb")
if not output then
  error("error " .. err)
end

print("saving to \"" .. filename .. ".dat\"")

bytes = nil

on_snoop = function(port, controller, index, value)
  if port == 1 and controller == 0 then
    if bytes == nil then bytes = 0 end
    bytes = bytes + bit.lshift(value, index)
  end


  if port == 0 and controller == 0 and index == 1 and value == 0 then
    if bytes ~= nil and output then
      output:write(string.char(bytes % 256, math.floor(bytes / 256)))
    end
    bytes = nil
  end

  if movie.framecount() < movie.currentframe() and output ~= nil then
    output:close()
    output = nil
    print("saved")
  end
end
