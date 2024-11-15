import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql

# Load Dataset
dataset = pd.read_csv(r"C:\Users\RG\OneDrive\Desktop\flexon data sets\day 1 data sets\tested.csv")

# Display Dataset Info
print("Dataset Info:")
dataset.info()

# Display Missing Values
print("\nMissing Values Count:")
print(dataset.isnull().sum())

# Display Shape
print("\nDataset Shape:", dataset.shape)

# Summary Statistics
print("\nSummary Statistics:")
print(dataset.describe())

# Head of Dataset
print("\nFirst 5 Rows of Dataset:")
print(dataset.head())

# Plot Missing Values Percentage
missing_percent = (dataset.isnull().sum() / len(dataset)) * 100
missing_percent = missing_percent[missing_percent > 0]

plt.figure(figsize=(10, 6))
missing_percent.plot(kind='bar', color='orange')
plt.title("Percentage of Missing Values by Column")
plt.xlabel("Columns")
plt.ylabel("Percentage of Missing Values")
plt.show()

# Fill Missing Values
dataset["Fare"] = dataset["Fare"].fillna(dataset["Fare"].mean())
dataset["Age"] = dataset["Age"].fillna(dataset["Age"].mean())

# Check Missing Values After Filling
print("\nMissing Values After Filling:")
print(dataset.isnull().sum())

# GroupBy Example
print("\nGroup By Example:")
dataset_groupby = dataset.groupby(['Pclass', 'Fare', 'Sex', 'Embarked']).size()
print(dataset_groupby)

# Aggregate Functions
print("\nAggregate Functions:")
grouped_agg = dataset.groupby(["Pclass", "Survived"]).agg({"Age": "mean", "Fare": "sum"})
print(grouped_agg)

# Pivot Table
pivot_table = dataset.pivot_table(index="Pclass", values=['Age', 'Fare'], aggfunc={"Age": 'mean', 'Fare': 'sum'})
print("\nPivot Table:")
print(pivot_table)

pivot_table.plot(kind='bar')
plt.title('Total Fare by Pclass')
plt.ylabel('Total Fare')
plt.xlabel('Pclass')
plt.show()

# Melt Dataset
dataset_melted = pd.melt(dataset, id_vars=['PassengerId', 'Survived'], var_name='Variable', value_name='Value')
print("\nMelted Dataset:")
print(dataset_melted.head())

# Split Dataset for Concatenation and Merging
dataset2 = dataset.iloc[:209]
dataset3 = dataset.iloc[209:]

# Concatenation
dataset_concatenated_rowwise = pd.concat([dataset2, dataset3], axis=0)
dataset_concatenated_colwise = pd.concat([dataset2, dataset3], axis=1)

# Merge
dataset_merged = pd.merge(dataset2, dataset3, on='Pclass', how='inner')

# Join
dataset2 = dataset2.set_index('PassengerId')
dataset3 = dataset3.set_index('PassengerId')
dataset_joined = dataset2.join(dataset3, how="outer", lsuffix='_left', rsuffix='_right')

# Stack
stacked_dataset = dataset.set_index(['PassengerId', 'Survived']).stack()

# Display Results
print("\nConcatenated Dataset (Row-wise):")
print(dataset_concatenated_rowwise.head())

print("\nConcatenated Dataset (Column-wise):")
print(dataset_concatenated_colwise.head())

print("\nMerged Dataset:")
print(dataset_merged.head())

print("\nJoined Dataset:")
print(dataset_joined.head())

print("\nStacked Dataset:")
print(stacked_dataset.head())

# MySQL Integration
conn = pymysql.connect(
    host="database-1.chk8ye4ga5gt.us-west-1.rds.amazonaws.com",
    port=3306,
    user="girish",
    password="girish99",
    database="titanic"
)
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS titanic (
    PassengerId INT PRIMARY KEY,
    Survived TINYINT,
    Pclass INT,
    Name VARCHAR(255),
    Sex VARCHAR(10),
    Age FLOAT,
    SibSp INT,
    Parch INT,
    Ticket VARCHAR(50),
    Fare FLOAT,
    Cabin VARCHAR(50),
    Embarked CHAR(1)
);
""")
conn.commit()
print("\nTable Created Successfully")

# Replace NaN with "Null"
dataset = dataset.where(pd.notnull(dataset), None)

# Insert Data into MySQL
sql = """
INSERT INTO titanic (
    PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

if not dataset.empty:
    values = [tuple(row) for row in dataset.values]
    cursor.executemany(sql, values)
    conn.commit()

cursor.close()
conn.close()
print("\nData Loaded Successfully into MySQL Database")

# Extract Data from MySQL
conn = pymysql.connect(
    host="database-1.chk8ye4ga5gt.us-west-1.rds.amazonaws.com",
    port=3306,
    user="girish",
    password="girish99",
    database="titanic"
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM titanic;")
data = cursor.fetchall()

columns = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
df = pd.DataFrame(data, columns=columns)

cursor.close()
conn.close()

print("\nExtracted Data from MySQL:")
print(df.head())

# Save Extracted Data to CSV
df.to_csv('extracted_data.csv', index=False)
print("\nExtracted Data Saved to CSV")
