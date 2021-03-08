import matplotlib as mpl
import matplotlib.pyplot as plt

import auxilary_tools as aux
from plots.pv_base_plotting import plot_vdiv_y_multi


def get_row_axes(big_ax, gs, index):
    return [big_ax.inset_axes(gs[index, i]) for i in range(gs.shape[1])]


def get_full_names(name):
    return "kg_vdiv_" + name


def get_row_big_axes(big_ax):
    gs = aux.loc(nrows=3, ncols=1, hs=0, vs=0.05, height_ratios=[1 / 3, 1 / 3, 1 / 3])
    print(gs.shape)
    row_big_axes = [big_ax.inset_axes(gs[i, 0]) for i in range(gs.shape[0])]
    for ax in row_big_axes:
        aux.clean_big_ax(ax)
    return row_big_axes


def plot_supp(names: list, texts: list, titles: list, figname: str):
    fnames = [[get_full_names(n) for n in names] for names in (names)]
    load_fun = aux.get_load_df_fun("simulation_data/transformed_kg_vdiv_scans")
    dsets_lists = [[load_fun(n) for n in names] for names in fnames]

    fig, big_ax = plt.subplots()
    aux.clean_big_ax(big_ax)
    row_big_axes = get_row_big_axes(big_ax)

    gs = aux.loc(3, 3, 0.02, 0.05, width_ratios=[1 / 3, 1 / 3, 1 / 3], height_ratios=[1 / 3, 1 / 3, 1 / 3])

    row_axes_lists = [get_row_axes(big_ax, gs, i) for i in range(gs.shape[0])]

    for dsets, row_axes in zip(dsets_lists, row_axes_lists):
        for dset, row_ax in zip(dsets, row_axes):
            plot_vdiv_y_multi(dset, "v_trans", row_ax)
    for i, axes in enumerate(row_axes_lists):
        for k, ax in enumerate(axes):
            if i != 0:
                ax.set_xlabel(None)
                ax.set_xticklabels([])
            if k != 0:
                ax.set_ylabel(None)
                ax.set_yticklabels([])
            ax.set_xticks([10, 20, 30, 40, 50])
            ax.set_xlim(9, 51)
            aux.make_grid(ax)

    for ax, title, let in zip(row_big_axes, titles, ["c", "b", "a"]):
        ax.set_title(title)
        ax.text(-0.07, 1.02, "({})".format(let), transform=ax.transAxes, fontsize=12)

    rates = dsets_lists[0][0].growth_rate
    cb_ax, kw = mpl.colorbar.make_axes(big_ax, fraction=0.1, aspect=40, pad=0.01)
    cb = aux.make_cb(cb_ax, values=rates, cmap=plt.cm.coolwarm, orientation="vertical")
    cb.ax.set_yticklabels(rates)
    cb.set_label("G1 growth rate [fL/min]")

    for text_list, axes in zip(texts, row_axes_lists):
        for text, ax in zip(text_list, axes):
            ax.text(0.98, 0.02, text, ha="right", va="bottom", transform=ax.transAxes, fontsize=8)


def plot_supp_sf():
    names = [["Whi5_50.pkl", "kpCln3_003.pkl", "Whi5_100.pkl"],
             ["kpCln3_002.pkl", "kpCLn3_003.pkl", "kpCln3_004.pkl"],
             ["kpCln3_0003_kd_00039.pkl", "kpCln3_003.pkl", "kpCln3_03_kd_039.pkl"]]

    texts = [["$n_0^{Whi5}=50$", "$n_0^{Whi5}=65$", "$n_0^{Whi5}=100$"],
             ["$k_p^{Cln3}=0.002$", "$k_p^{Cln3}=0.003$", "$k_p^{Cln3}=0.004$"],
             ["$k_p^{Cln3}=0.0003$\n$k_d^{Cln3}=0.00039$", "$k_p^{Cln3}=0.003$\n$k_d^{Cln3}=0.0039$",
              "$k_p^{Cln3}=0.03$\n$k_d^{Cln3}=0.039$"]]

    titles = ["initial amount of Whi5 [a.u.]",
              "Cln3 production rate [a.u./s], $k_d=0.0039$ a.u./s",
              "speed of Cln3 approaching steady state ($k_p$, $k_d$ in a.u./s)"]

    plot_supp(names, texts, titles, "kg_vdiv_supp_sf.pdf")


def plot_supp_st():
    names = [["Whi5_50_st.pkl", "Whi5_65_st.pkl", "Whi5_100_st.pkl"],
             ["nHill_2.pkl", "nHill_10.pkl", "nHill_20.pkl"],
             ["Whi5_65_st.pkl", "Khill_17.pkl", "Khill_19.pkl"]]

    texts = [["$n_0^{Whi5}=50$", "$n_0^{Whi5}=65$", "$n_0^{Whi5}=100$"],
             ["$n_H=2$", "$n_H=10$", "$n_H=20$"],
             ["$K_H=$1.5e-6", "$K_H=1.7$e-6", "$K_H=1.9$e-6"]]

    titles = ["initial amount of Whi5 [a.u.]",
              "Hill coefficient",
              "Hill constant [Pa]"]

    plot_supp(names, texts, titles, "kg_vdiv_supp_st.pdf")


if __name__ == "__main__":
    f = 2
    mpl.rc('axes', labelsize=8, titlesize=9, linewidth=0.8 / f, labelpad=4.0 / f, titlepad=6 / f)
    mpl.rc('lines', linewidth=1.5 / f, markersize=8 / f, markeredgewidth=1.5 / f)
    mpl.rc('xtick', labelsize=8)
    mpl.rc('xtick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick.major', size=3.5 / f, width=0.8 / f, pad=0.8 / f)
    mpl.rc('ytick', labelsize=8)
    mpl.rc('legend', frameon=False, fontsize=7, borderpad=0.4 / f, labelspacing=0.5 / f, handlelength=2 / f,
           handleheight=0.7 / f, handletextpad=0.8 / f, borderaxespad=0.5 / f)
    mpl.rc('figure', figsize=(17 / 2.54, 17 / 2.54), dpi=300)

    plot_supp_sf()
    plot_supp_st()

    plt.show()
