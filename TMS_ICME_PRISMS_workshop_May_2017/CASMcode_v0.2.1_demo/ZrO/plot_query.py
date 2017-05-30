from casm.project import Project, Selection, write_eci
import matplotlib.pyplot as plt

# construct a 'Selection'
proj = Project()
sel = Selection(proj, 'CALCULATED', all=False)

# query results into a pandas.DataFrame
comp = 'comp(a)'
Ef = 'formation_energy'
hull_dist = 'hull_dist(CALCULATED,atom_frac)'
sel.query([comp, Ef, hull_dist])

# get convex hull configurations, sorted for nice plotting
df = sel.data.sort_values([comp])
hull_tol = 1e-6
df_hull = df[df[hull_dist] < hull_tol]
print df_hull.to_string()

# plot formation energies with convex hull
plt.scatter(sel.data[comp], sel.data[Ef],  marker='o')
plt.plot(df_hull[comp], df_hull[Ef], 'b.-')
plt.xlabel(comp)
plt.ylabel('Formation energy (eV/unit cell)')
plt.xlim([0.,1.])
plt.show()