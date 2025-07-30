import matplotlib.pyplot as plt
import seaborn as sns
import os

def discharge_vs_time(results, folder):
    fig, ax = plt.subplots(1, 2, figsize=(6,3))
    for index in results.index:
        if results['Battery chemistry'][index] == 'NCA-Gr':
            color = 'tab:blue'
        else:
            color = 'tab:orange'
        t = results['Life simulation outputs'][index]['Time (days)']
        efc = results['Life simulation outputs'][index]['Time (days)']
        q = results['Life simulation outputs'][index]['Relative discharge capacity']
        ax[0].plot(t/365, q, color=color, alpha=0.5)
        ax[1].plot(efc, q, color=color, alpha=0.5)
    ax[0].set_xlabel('Time (years)')
    ax[0].set_ylabel('Relative discharge capacity')
    ax[0].set_xlim([0, 20])
    ax[1].set_yticklabels([])
    ax[1].set_xlabel('Equivalent full cycles')
    ax[1].set_xlim([0, 10000])
    plt.savefig(os.path.join(folder, 'output1'), bbox_inches='tight')
    #plt.savefig('Discharge_capacity_vs_time', bbox_inches = 'tight')

def milesto80_vs_x(results, folder):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1: Miles to 80% vs Throughput
    sns.scatterplot(data=results, y='Miles to 80% capacity',
                    x='Total energy throughput per mile (kWh/mi)',
                    hue='Pack size', style='Battery chemistry',
                    palette='tab10', ax=axes[0])
    axes[0].set_xlabel('Total energy throughput\nper mile (kWh/mi)')
    axes[0].set_ylabel('Miles to 80% capacity')
    axes[0].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

    # Plot 2: Miles to 80% vs Total Miles
    sns.scatterplot(data=results, y='Miles to 80% capacity',
                    x='Total miles (mi)',
                    hue='Pack size', style='Battery chemistry',
                    palette='tab10', ax=axes[1])
    axes[1].set_xlabel('Total miles (mi)')
    axes[1].set_ylabel('')
    axes[1].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

    # Plot 3: Miles to 80% vs Max Microtrip RMS Power
    sns.scatterplot(data=results, y='Miles to 80% capacity',
                    x='Max Microtrip RMS Power (kW)',
                    hue='Pack size', style='Battery chemistry',
                    palette='tab10', ax=axes[2])
    axes[2].set_xlabel('Max Microtrip RMS Power (kW)')
    axes[2].set_ylabel('')
    axes[2].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

    # Remove legends from subplots
    for ax in axes:
        if ax.get_legend():
            ax.get_legend().remove()

    # Create a single legend above the plots
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels,
               loc='upper center',
               bbox_to_anchor=(0.5, 1.15),
               ncol=3,
               title='Pack size / Battery chemistry')

    # Create extra space at the top for the legend
    fig.subplots_adjust(top=0.85)

    # Save the figure
    plt.savefig(os.path.join(folder, 'output2.png'), bbox_inches='tight')

def count_graphs(results, folder):
    fig, axes = plt.subplots(1, 2, figsize=(6, 3))  # Two side-by-side subplots

    # Plot 1: Miles to 80% capacity
    sns.histplot(data=results, x='Miles to 80% capacity',
                 hue='Battery chemistry', ax=axes[0])
    axes[0].set_title('Miles to 80% capacity')
    axes[0].set_xlabel('Miles')
    axes[0].set_ylabel('Count')

    # Plot 2: Years to 80% capacity
    sns.histplot(data=results, x='Years to 80% capacity',
                 hue='Battery chemistry', ax=axes[1])
    axes[1].set_title('Years to 80% capacity')
    axes[1].set_xlabel('Years')
    axes[1].set_ylabel('')

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(os.path.join(folder, 'output3'), bbox_inches='tight')

def packsize_boxplots(results, folder):
    fig, axes = plt.subplots(1, 2, figsize=(10, 3))  # Two subplots side by side

    # Plot 1: Miles to 80% capacity vs Pack size
    sns.boxplot(data=results, x='Pack size', y='Miles to 80% capacity',
                hue='Battery chemistry', ax=axes[0])
    axes[0].set_xlabel('Pack size (kWh)')
    axes[0].set_ylabel('Miles to 80% capacity')
    axes[0].set_title('Miles vs Pack Size')
    sns.move_legend(axes[0], "upper left", bbox_to_anchor=(1.05, 1), frameon=False)

    # Plot 2: Years to 80% capacity vs Pack size
    sns.boxplot(data=results, x='Pack size', y='Years to 80% capacity',
                hue='Battery chemistry', ax=axes[1])
    axes[1].set_xlabel('Pack size (kWh)')
    axes[1].set_ylabel('Years to 80% capacity')
    axes[1].set_title('Years vs Pack Size')
    sns.move_legend(axes[1], "upper left", bbox_to_anchor=(1.05, 1), frameon=False)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, 'output4'), bbox_inches='tight')

def charge_event_plots(results, folder):
    fig, ax = plt.subplots(1, 2, figsize=[6, 3])

    # Histogram: Initial vs Final charge events
    sns.histplot(data=results, x='Initial charge events', ax=ax[0], binwidth=1, label='Initial')
    sns.histplot(data=results, x='Final charge events', ax=ax[0], binwidth=1, label='Final')
    ax[0].set_xlabel('Charge events')
    ax[0].set_ylabel('Count')
    ax[0].legend()
    ax[0].set_title('Charge Events Histogram')

    # Melt the dataframe for boxplot
    results_df_melt = results.melt(
        id_vars=['Summary file idx', 'Pack size'],
        value_vars=['Initial charge events', 'Final charge events'],
        var_name='Charge event indicator',
        value_name='Charge events'
    )

    # Boxplot: Charge events by pack size
    sns.boxplot(data=results_df_melt, x='Pack size', y='Charge events',
                hue='Charge event indicator', ax=ax[1])
    ax[1].set_xlabel('Pack size (kWh)')
    ax[1].set_ylabel('Charge events')
    ax[1].legend(title=None)
    ax[1].set_title('Charge Events by Pack Size')

    plt.tight_layout()
    plt.savefig(os.path.join(folder, 'output5'), bbox_inches='tight')

def ecdf_charge_events_plot(results, folder):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    sns.ecdfplot(data=results, x='Initial charge events',
                 hue='Pack size', palette='tab10', ax=ax)

    ax.set_xlabel('Initial charge events')
    ax.set_ylabel('ECDF')
    ax.set_title('ECDF of Initial Charge Events')

    #sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1), frameon=False)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, 'output6'), bbox_inches='tight')

def ecdf_and_box_charge_events(results, folder):
    fig, ax = plt.subplots(1, 2, figsize=[6, 3])

    # ECDF Plot: Initial vs Final
    sns.ecdfplot(data=results, x='Initial charge events', ax=ax[0], label='Initial')
    sns.ecdfplot(data=results, x='Final charge events', ax=ax[0], label='Final')
    ax[0].set_xlabel('Charge events')
    ax[0].set_ylabel('ECDF')
    ax[0].set_title('ECDF of Charge Events')
    ax[0].legend()

    # Melt data for boxplot
    results_df_melt = results.melt(
        id_vars=['Summary file idx', 'Pack size'],
        value_vars=['Initial charge events', 'Final charge events'],
        var_name='Charge event indicator',
        value_name='Charge events'
    )

    # Boxplot: Charge events vs Pack size
    sns.boxplot(data=results_df_melt, x='Pack size', y='Charge events',
                hue='Charge event indicator', ax=ax[1])
    ax[1].set_xlabel('Pack size (kWh)')
    ax[1].set_ylabel('Charge events')
    ax[1].set_title('Charge Events by Pack Size')
    ax[1].legend(title=None)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, 'output7'), bbox_inches='tight')

def final_charge_vs_miles_plot(results, folder):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    sns.scatterplot(data=results,
                    x='Total miles (mi)',
                    y='Final charge events',
                    hue='Pack size',
                    style='Battery chemistry',
                    palette='tab10',
                    ax=ax)

    ax.set_xlabel('Total miles (mi)')
    ax.set_ylabel('Final charge events')
    ax.set_title('Final Charge Events vs Total Miles')

    plt.tight_layout()
    plt.savefig(os.path.join(folder, 'output8'), bbox_inches='tight')

def charge_event_increase_boxplot(results, folder):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    sns.boxplot(data=results,
                x='Pack size',
                y='% increase in charge events',
                hue='Battery chemistry',
                ax=ax)

    ax.set_xlabel('Pack size (kWh)')
    ax.set_ylabel('% Increase in Charge Events')
    ax.set_title('Increase in Charge Events by Pack Size')

    plt.tight_layout()
    plt.savefig(os.path.join(folder, 'output9'), bbox_inches='tight')

def create_plots(results, folder):
    # Finds how many folders up the chain exist
    base_folder = folder
    counter = 1
    while os.path.exists(folder):
        folder = f"{base_folder} ({counter})"
        counter += 1

    os.makedirs(folder)

    # Plot everything in the created folder
    discharge_vs_time(results, folder)
    milesto80_vs_x(results, folder)
    count_graphs(results, folder)
    packsize_boxplots(results, folder)
    charge_event_plots(results, folder)
    ecdf_charge_events_plot(results, folder)
    ecdf_and_box_charge_events(results, folder)
    final_charge_vs_miles_plot(results, folder)
    charge_event_increase_boxplot(results, folder)

    print(f"Plots saved in folder: {folder}")