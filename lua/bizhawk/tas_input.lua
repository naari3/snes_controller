-- tas input
-- bizhawk
-- only still 1P

function inputToInt (inputs)
	bytesLow = 0
	bytesHigh = 0

	-- 4321RLXArlduSsYB
	if inputs["P1 B"]      then bytesLow = bytesLow + 0x01 end
	if inputs["P1 Y"]      then bytesLow = bytesLow + 0x02 end
	if inputs["P1 Select"] then bytesLow = bytesLow + 0x04 end
	if inputs["P1 Start"]  then bytesLow = bytesLow + 0x08 end
	if inputs["P1 Up"]     then bytesLow = bytesLow + 0x10 end
	if inputs["P1 Down"]   then bytesLow = bytesLow + 0x20 end
	if inputs["P1 Left"]   then bytesLow = bytesLow + 0x40 end
	if inputs["P1 Right"]  then bytesLow = bytesLow + 0x80 end

	if inputs["P1 A"]      then bytesHigh = bytesHigh + 0x01 end
	if inputs["P1 X"]      then bytesHigh = bytesHigh + 0x02 end
	if inputs["P1 L"]      then bytesHigh = bytesHigh + 0x04 end
	if inputs["P1 R"]      then bytesHigh = bytesHigh + 0x08 end

	-- 1234id is still not implemented

	return bytesLow, bytesHigh
end


local output = io.open(gameinfo.getromname() .. ".dat", "wb")

console.log("saving to \"" .. gameinfo.getromname() .. ".dat\"")

if movie.isloaded() then
	while movie.mode() == "PLAY" do
		if not emu.islagged() then
			output:write(string.char(inputToInt(movie.getinput(i))))
		end
	end
end

output:close()
