class UdpPacket():
	MAX_SIZE = 200
	MSG_TYPE_WITH_ACK = 0x1
	MSG_TYPE_NO_ACK = 0x2
	MSG_TYPE_ACK = 0x3

	CMD_TYPE_INSTANTIATE = 0x1
	CMD_TYPE_DELETE = 0x2
	CMD_TYPE_TRANSFORM_AND_PARAMS = 0x3
	CMD_TYPE_CHAT = 0x4

	def create(msgType, cmdType, data):
		if len(data) > MAX_SIZE-2:
			print('[Error]: Trying to send too big UdpPacket')
			return
		self.packet = bytes[2]
		self.packet[0] = msgType
		self.packet[1] = cmdType
		self.packet += data
		return data

	def __init__(self, packet):
		self.packet = packet
		self.cmdType = packet[1]
	def needAck(self):
		if self.packet[0] != UdpPacket.MSG_TYPE_WITH_ACK:
			return False
		return True
	def getData(self):
		data = bytearray(self.data)
		del data[0]
		del data[1]
		return data

