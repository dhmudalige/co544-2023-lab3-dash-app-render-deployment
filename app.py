# Import relevant libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import plotly.express as px

import dash

import dash_bootstrap_components as dbc

from dash import dcc, html
from dash.dependencies import Input, Output, State

 # Load dataset
data = pd.read_csv('data/winequality-red.csv')
# Check for missing values
data.isna().sum()
# Remove duplicate data
data.drop_duplicates(keep='first')
# Calculate the correlation matrix
corr_matrix = data.corr()
# Label quality into Good (1) and Bad (0)
data['quality'] = data['quality'].apply(lambda x: 1 if x >= 6.0 else 0)
    # Drop the target variable
X = data.drop('quality', axis=1)
# Set the target variable as the label
y = data['quality']


# Split the dat a into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
# Create an instance of the logistic regression model
logreg_model = LogisticRegression()
# Fit the model to the training data
logreg_model.fit(X_train, y_train)

# Predict the labels of the test set
# y_pred = logreg_model.predict(X_test)


# Create the Dash app
# app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define the layout of the dashboard
app.layout = html.Div(
    children=[
    
    html.H1('CO544-2023 Lab 3: Wine Quality Prediction'),
    html.Br(),

    html.Div([
        html.H3('Exploratory Data Analysis'),
        html.Br(),    
        html.Label('Feature 1 (X-axis)'),
        dcc.Dropdown(
            id='x_feature',
            options=[{'label': col, 'value': col} for col in data.columns],
            value=data.columns[0]
        )
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    html.Div([
        html.Label('Feature 2 (Y-axis)'),
        dcc.Dropdown(
            id='y_feature',
            options=[{'label': col, 'value': col} for col in data.columns],
            value=data.columns[1]
        )
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    dcc.Graph(id='correlation_plot'),
    
    # Wine quality prediction based on input feature values
    html.H3("Wine Quality Prediction"),

    html.Table([
        html.Tr([
            html.Td([
                html.Label("Fixed Acidity"),
                dcc.Input(value=9.1,id='fixed_acidity', type='number', required=True)
            ]),
            
            html.Td([
                html.Label("Volatile Acidity"),
                dcc.Input(value=0.44,id='volatile_acidity', type='number', required=True)
            ]),
            
            html.Td([
                html.Label("Citric Acid"),
                dcc.Input(value=0.5,id='citric_acid', type='number', required=True)
            ])       
        ], style = {
        'padding': 10
        }),
            
        html.Tr([
            html.Td([
                html.Label("Residual Sugar"),
                dcc.Input(value=1.7,id='residual_sugar', type='number', required=True)
            ]),
            html.Td([
                html.Label("Chlorides"),
                dcc.Input(value=0.071,id='chlorides', type='number', required=True)
            ]),
            html.Td([
                html.Label("Free Sulfur Dioxide"),
                dcc.Input(value=6.9,id='free_sulfur_dioxide', type='number', required=True)
            ])
        ], style = {
        'padding': 10
        }),

        html.Tr([
            html.Td([
                html.Label("Total Sulfur Dioxide"),
                dcc.Input(value=15.0,id='total_sulfur_dioxide', type='number', required=True)
            ]),
            html.Td([
                html.Label("Density"),
                dcc.Input(value=0.995,id='density', type='number', required=True)
            ]),
            html.Td([
                html.Label("pH"),
                dcc.Input(value=3.11,id='ph', type='number', required=True),
            ])
        ], style = {
        'padding': 10
        }),
            
        html.Tr([
            html.Td([
                html.Label("Sulphates"),
                dcc.Input(value=0.7,id='sulphates', type='number', required=True)
            ]),
            html.Td([
                html.Label("Alcohol"),
                dcc.Input(value=11.9,id='alcohol', type='number', required=True)
            ])
        ], style = {
        'padding': 10
        })

    ]),

    html.Br(),
    
    html.Div([
        html.Button('Predict', id='predict-button', n_clicks=0),
    ]),

    html.Br(),
    html.Br(),

    html.Div([
        html.H4("Predicted Quality"),
        html.Br(),
        dbc.Alert(id='prediction-output', color="warning")
        # html.Div(id='prediction-output')
    ])
])

# Define the callback to update the correlation plot
@app.callback(
    dash.dependencies.Output('correlation_plot', 'figure'),
    [dash.dependencies.Input('x_feature', 'value'),
     dash.dependencies.Input('y_feature', 'value')]
)
def update_correlation_plot(x_feature, y_feature):
    fig = px.scatter(data, x=x_feature, y=y_feature, color='quality')
    fig.update_layout(title=f"Correlation between {x_feature} and {y_feature}")
    return fig

# Define the callback function to predict wine quality
@app.callback(
    Output(component_id='prediction-output', component_property='children'),
    [Input('predict-button', 'n_clicks')],
    [State('fixed_acidity', 'value'),
     State('volatile_acidity', 'value'),
     State('citric_acid', 'value'),
     State('residual_sugar', 'value'),
     State('chlorides', 'value'),
     State('free_sulfur_dioxide', 'value'),
     State('total_sulfur_dioxide', 'value'),
     State('density', 'value'),
     State('ph', 'value'),
     State('sulphates', 'value'),
     State('alcohol', 'value')]
)
def predict_quality(n_clicks, fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                     chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol):
    # Create input features array for prediction
    input_features = np.array([fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, 
                               free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol]).reshape(1, -1)

    # Predict the wine quality (0 = bad, 1 = good)
    prediction = logreg_model.predict(input_features)[0]

    # Return the prediction
    if prediction == 1:
        return 'This wine is predicted to be good quality.'
    else:
        return 'This wine is predicted to be bad quality.'


if __name__ == '__main__':
    app.run_server(debug=False)