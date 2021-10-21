import pkmodel as pk

protocol = pk.Protocol('pkmodel/config_file.txt')
model = protocol.generate_model()
x = model.solve()

x.output()


