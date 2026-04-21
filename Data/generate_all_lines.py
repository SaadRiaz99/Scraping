import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def generate_individual_line_graphs():
    # 1. Find all CSV files in the current directory
    csv_files = glob.glob("*.csv")
    output_dir = "individual_graphs"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Found {len(csv_files)} CSV files. Generating individual line graphs...")

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]
        
        try:
            # Read the data (taking first 150 rows for clarity if file is large)
            df = pd.read_csv(file_path)
            if len(df) > 150:
                df = df.head(150)
                subset_msg = "(First 150 records)"
            else:
                subset_msg = ""

            # Find numeric columns to plot
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) < 1:
                print(f"Skipping {file_name}: No numeric data found.")
                continue

            # Create the plot
            plt.figure(figsize=(12, 6))
            
            # Plot the first main numeric column (usually the target or key metric)
            # For our specific files, this handles scores, usage hours, or bounce rates.
            target_col = numeric_cols[-1] # Usually the last column is the target (Score, Revenue, etc.)
            
            plt.plot(df.index, df[target_col], marker='o', markersize=3, linestyle='-', color='teal', linewidth=1.5)
            
            plt.title(f"Individual Line Graph: {base_name}\n{target_col} Trend {subset_msg}")
            plt.xlabel("Record Index")
            plt.ylabel(target_col)
            plt.grid(True, alpha=0.3)
            
            # Save the individual graph
            output_path = os.path.join(output_dir, f"{base_name}_line.png")
            plt.savefig(output_path)
            plt.close()
            
            print(f"✅ Created: {output_path}")

        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")

if __name__ == "__main__":
    generate_individual_line_graphs()
    print("\nAll individual graphs are ready in the 'individual_graphs' folder.")
