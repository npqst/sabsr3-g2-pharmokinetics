import pkmodel as pk
import matplotlib.pyplot as plt


protocol = pk.Protocol('pkmodel/config_file.txt')
model = protocol.generate_model()
x = model.solve()

print(x.get_solution)
print(x.get_solution.y.shape)


#TODO: move plotting to solution class
plt.figure()

y1 = x.get_solution.y[0, :]
y2 = x.get_solution.y[1, :]
y3 = x.get_solution.y[2, :]
y4 = x.get_solution.y[3, :]
t = x.get_solution.t
plt.plot(t, y1, t, y2, t, y3, t, y4)
plt.legend(['y1', 'y2', 'y3'])
plt.show()
