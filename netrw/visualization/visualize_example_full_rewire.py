import matplotlib.pyplot as plt

plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
plt.rc("axes", axisbelow=True)


def visualize_example_full_rewire(
    RewiringTechnique=LocalEdgeRewiring,
    rewiring_technique_label="Local edge rewire",
    list_of_graphs=[],
    timesteps=100,
    save_fig=False,
    save_fig_folder="",
    save_fig_filename="",
):
    """
    This is a useful function for visualizing outputs from repeated runs of
    `step_rewire`. Users can use this to get a sense of what is happening
    structurally to the graph as the algorithm progresses.

    Parameters
    ----------
    RewiringTechnique (netrw.rewire method)
        Feed in the name of the rewiring technique to look at.
    rewiring_technique_label (str)
        Label of the technique (for a title in the plot)
    list_of_graphs (list of nx.Graph objects)
        List of graphs to visualize repeated `step_rewire` iterations.
        Recommended number = 2-6 graphs, otherwise the plot might get crazy.
        If no list of graphs are input, the function defaults to six relatively
        diverse networks to test it on.
    timesteps (int)
        Number of timesteps to iterate `step_rewire`
    save_fig (bool)
        If False, the function just shows the matplotlib figure
    save_fig_folder (str)
        If the user wants to specify the specific output folder.
    save_fig_filename (str)
        If the user wants to name the saved figure something different than
        just the name of the rewiring technique. Additionally, if the filetype
        is not specified, it defaults to .png

    Returns
    -------
    Either a saved image or a plt.show() instance.

    """

    if list_of_graphs == []:
        list_of_graphs = [
            nx.karate_club_graph(),
            nx.ring_of_cliques(4, 16),
            nx.random_geometric_graph(50, 0.2),
            nx.erdos_renyi_graph(50, 0.05),
            nx.erdos_renyi_graph(50, 0.30),
            nx.barabasi_albert_graph(50, 2),
        ]

    # example params for node sizes, edge widths, etc.
    ns = 100
    lw = 2
    ew = 2.5
    n_ec = ".3"

    # fig width and height
    base_width = 5
    base_height = 5

    fig, ax = plt.subplots(
        len(list_of_graphs),
        2,
        figsize=(base_width * 2, base_height * len(list_of_graphs)),
        dpi=100,
    )

    ax[(0, 0)].text(
        1.1,
        1.2,
        "Method: " + rewiring_technique_label,
        ha="center",
        va="center",
        transform=ax[(0, 0)].transAxes,
        fontsize="xx-large",
    )

    for ix, G0 in enumerate(list_of_graphs):

        pos = nx.kamada_kawai_layout(G0)
        G = G0.copy()

        for _ in range(timesteps):
            G = RewiringTechnique().step_rewire(G)

        # draw original network
        nx.draw_networkx_nodes(
            G0,
            pos,
            ax=ax[(ix, 0)],
            node_size=ns,
            node_color="w",
            edgecolors=n_ec,
            linewidths=lw,
        )
        nx.draw_networkx_edges(
            G0, pos, ax=ax[(ix, 0)], edge_color=".5", width=ew, alpha=0.35
        )

        # draw rewired network
        nx.draw_networkx_nodes(
            G,
            pos,
            ax=ax[(ix, 1)],
            node_size=ns,
            node_color="w",
            edgecolors=n_ec,
            linewidths=lw,
        )
        nx.draw_networkx_edges(
            G, pos, ax=ax[(ix, 1)], edge_color=".5", width=ew, alpha=0.35
        )

        ax[(ix, 0)].set_title("Original network")
        ax[(ix, 1)].set_title("Rewired network (n=%i timesteps)" % timesteps)

    if save_fig:
        if save_fig_filename == "":
            save_fig_filename = rewiring_technique_label.lower().replace(" ", "_")

        if save_fig_filename[-4:] != ".png" and save_fig_filename[-4:] != ".pdf":
            save_fig_filename = save_fig_filename + ".png"

        fn = save_fig_folder + save_fig_filename
        print(fn)
        plt.savefig(fn, dpi=300, bbox_inches="tight")
        plt.close()

    else:
        plt.show()
