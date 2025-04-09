import pandas as pd
import os

def process_sales_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Filter for Pink Morsels only (case insensitive)
    df = df[df['product'].str.lower() == 'pink morsel']
    
    # Remove the '$' from price and convert to float
    df['price'] = df['price'].str.replace('$', '').astype(float)
    
    # Calculate sales
    df['sales'] = df['price'] * df['quantity']
    
    # Select only the required columns
    df = df[['sales', 'date', 'region']]
    
    return df

def main():
    # Path to data directory
    data_dir = 'data'
    
    # List to store all dataframes
    dfs = []
    
    # Process each CSV file
    for i in range(3):
        file_path = os.path.join(data_dir, f'daily_sales_data_{i}.csv')
        df = process_sales_data(file_path)
        dfs.append(df)
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Sort by date and region
    combined_df = combined_df.sort_values(['date', 'region'])
    
    # Save the processed data
    output_path = os.path.join(data_dir, 'processed_sales_data.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    main() 