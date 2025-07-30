import torch
import torch.nn.functional as F
from torch_geometric.nn import MessagePassing, global_mean_pool
from torch_geometric.data import Data

class PerovskiteGNN(MessagePassing):
    """Graph Neural Network for predicting perovskite properties."""
    def __init__(self, node_input_dim, edge_input_dim, hidden_dim, output_dim):
        super(PerovskiteGNN, self).__init__(aggr='add')
        self.node_encoder = torch.nn.Linear(node_input_dim, hidden_dim)
        self.edge_encoder = torch.nn.Linear(edge_input_dim, hidden_dim)
        self.conv1 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.conv2 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.conv3 = torch.nn.Linear(hidden_dim, hidden_dim)
        self.fc = torch.nn.Linear(hidden_dim, output_dim)

    def forward(self, data: Data):
        x, edge_index, edge_attr, batch = data.x, data.edge_index, data.edge_attr, data.batch

        x = self.node_encoder(x)
        edge_attr = self.edge_encoder(edge_attr)

        x = F.relu(self.propagate(edge_index, x=x, edge_attr=edge_attr))
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        
        x = global_mean_pool(x, batch)
        
        return self.fc(x)

    def message(self, x_j, edge_attr):
        return x_j + edge_attr