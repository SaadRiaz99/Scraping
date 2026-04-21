import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def generate_graphs():
    # 1. Configuration
    input_folder = "csv_data"
    output_folder = "output_graphs"
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 2. Find all CSV files automatically
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    
    if not csv_files:
        print("No CSV files found in 'csv_data' folder.")
        return

    print(f"Found {len(csv_files)} files. Starting visualization...")

    for file_path in csv_files:
        # Get the filename without extension for naming graphs
        file_name = os.path.basename(file_path).split('.')[0]
        
        try:
            # 3. Read the Data
            # Assumes 1st column is labels (X) and 2nd column is values (Y)
            df = pd.read_csv(file_path)
            
            # Identify columns
            x_col = df.columns[0]
            y_col = df.columns[1]

            # 4. Generate Bar Chart
            plt.figure(figsize=(10, 6))
            plt.bar(df[x_col], df[y_col], color='skyblue', edgecolor='navy')
            plt.title(f"Bar Chart: {file_name}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{output_folder}/{file_name}_bar.png")
            plt.close() # Close to free up memory

            # 5. Generate Line Graph
            plt.figure(figsize=(10, 6))
            plt.plot(df[x_col], df[y_col], marker='o', color='red', linestyle='-', linewidth=2)
            plt.title(f"Line Graph: {file_name}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig(f"{output_folder}/{file_name}_line.png")
            plt.close()

            print(f"✅ Generated graphs for: {file_name}")

        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")

if __name__ == "__main__":
    generate_graphs()
    print("\nAll tasks complete! Check the 'output_graphs' folder.")
