import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

def generate_dual_visuals():
    csv_files = glob.glob("*.csv")
    output_dir = "individual_graphs"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Processing {len(csv_files)} real-world files for Line & Bar visualizations...")

    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]
        
        try:
            df = pd.read_csv(file_path)
            # Use top 150 for line trends, but full data for bar averages
            line_df = df.head(150) if len(df) > 150 else df
            
            # Find columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            categorical_cols = df.select_dtypes(include=['object', 'bool']).columns
            
            if len(numeric_cols) < 1:
                continue

            target_val = numeric_cols[-1] # The metric (Score, Revenue, etc.)
            
            # Create a 2-part visualization (1 row, 2 columns)
            plt.figure(figsize=(20, 8))
            
            # --- 1. THE LINE GRAPH (Trend) ---
            plt.subplot(1, 2, 1)
            plt.plot(line_df.index, line_df[target_val], color='teal', linewidth=1, marker='o', markersize=2)
            plt.title(f"Real-time Line Trend: {base_name}\n({target_val})", fontsize=14)
            plt.xlabel("Record Index")
            plt.ylabel(target_val)
            plt.grid(True, alpha=0.3)

            # --- 2. THE BAR GRAPH (Categorical Comparison) ---
            plt.subplot(1, 2, 2)
            if len(categorical_cols) > 0:
                # Use the first categorical column to group data (e.g., Gender, VisitorType)
                cat_col = categorical_cols[0]
                avg_data = df.groupby(cat_col)[target_val].mean().reset_index()
                sns.barplot(x=cat_col, y=target_val, data=avg_data, palette='viridis')
                plt.title(f"Real-time Comparison: {target_val} by {cat_col}", fontsize=14)
            else:
                # If no categories, show top 15 individual records
                sample_df = df.head(15)
                plt.bar(sample_df.index.astype(str), sample_df[target_val], color='orange')
                plt.title(f"Comparison: Individual {target_val} (Top 15)", fontsize=14)
            
            plt.ylabel(f"Average {target_val}")
            plt.xticks(rotation=45)

            # Save combined visual
            output_path = os.path.join(output_dir, f"{base_name}_dual_report.png")
            plt.tight_layout()
            plt.savefig(output_path)
            plt.close()
            
            print(f"✅ Generated Dual Report: {output_path}")

        except Exception as e:
            print(f"❌ Error on {file_name}: {e}")

if __name__ == "__main__":
    generate_dual_visuals()
    print("\nAll reports are updated with Line and Bar graphs.")
