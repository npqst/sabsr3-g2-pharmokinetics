import pkmodel as pk

protocol = pk.Protocol()
model = protocol.generate_model()
x = model.solve()

x.output()
