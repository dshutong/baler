# Copyright 2022 Baler Contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import torch
from torch import nn
from torch.nn import functional as F


class AE(nn.Module):
    # This class is a modified version of the original class by George Dialektakis found at
    # https://github.com/Autoencoders-compression-anomaly/Deep-Autoencoders-Data-Compression-GSoC-2021
    # Released under the Apache License 2.0 found at https://www.apache.org/licenses/LICENSE-2.0.txt
    # Copyright 2021 George Dialektakis

    def __init__(self, n_features, z_dim, *args, **kwargs):
        super(AE, self).__init__(*args, **kwargs)

        # encoder
        self.en1 = nn.Linear(n_features, 200, dtype=torch.float64)
        self.en2 = nn.Linear(200, 100, dtype=torch.float64)
        self.en3 = nn.Linear(100, z_dim, dtype=torch.float64)

        # decoder
        self.de1 = nn.Linear(z_dim, 100, dtype=torch.float64)
        self.de2 = nn.Linear(100, 200, dtype=torch.float64)
        self.de3 = nn.Linear(200, n_features, dtype=torch.float64)

        self.n_features = n_features
        self.z_dim = z_dim

    def encode(self, x):
        h1 = F.leaky_relu(self.en1(x))
        h2 = F.leaky_relu(self.en2(h1))
        z = self.en3(h2)
        return z

    def decode(self, z):
        h8 = F.leaky_relu(self.de1(z))
        h9 = F.leaky_relu(self.de2(h8))
        out = self.de3(h9)

        return out

    def forward(self, x):
        z = self.encode(x)
        return self.decode(z)




class AE_Dropout_BN(nn.Module):
    def __init__(self, n_features, z_dim, *args, **kwargs):
        super(AE_Dropout_BN, self).__init__(*args, **kwargs)

        # encoder
        self.enc_nn = nn.Sequential(
            nn.Linear(n_features, 200, dtype=torch.float64),
            nn.Dropout(p=0.5),
            nn.LeakyReLU(),
            # nn.BatchNorm1d(200,dtype=torch.float64),
            nn.Linear(200, 100, dtype=torch.float64),
            nn.Dropout(p=0.4),
            nn.LeakyReLU(),
            # nn.BatchNorm1d(100,dtype=torch.float64),
            nn.Linear(100, 50, dtype=torch.float64),
            nn.Dropout(p=0.3),
            nn.LeakyReLU(),
            # nn.BatchNorm1d(50,dtype=torch.float64),
            nn.Linear(50, z_dim, dtype=torch.float64),
            nn.Dropout(p=0.2),
            nn.LeakyReLU(),
            # nn.BatchNorm1d(z_dim,dtype=torch.float64)
        )

        # decoder
        self.dec_nn = nn.Sequential(
            nn.Linear(z_dim, 50, dtype=torch.float64),
            # nn.Dropout(p=0.2),
            nn.LeakyReLU(),
            nn.BatchNorm1d(50, dtype=torch.float64),
            nn.Linear(50, 100, dtype=torch.float64),
            # nn.Dropout(p=0.3),
            nn.LeakyReLU(),
            nn.BatchNorm1d(100, dtype=torch.float64),
            nn.Linear(100, 200, dtype=torch.float64),
            # nn.Dropout(p=0.4),
            nn.LeakyReLU(),
            nn.BatchNorm1d(200, dtype=torch.float64),
            nn.Linear(200, n_features, dtype=torch.float64),
            # nn.Dropout(p=0.5),
            nn.BatchNorm1d(n_features, dtype=torch.float64),
            nn.ReLU(),
        )

        self.n_features = n_features
        self.z_dim = z_dim

    def encode(self, x):
        out = self.enc_nn(x)
        return out

    def decode(self, z):
        out = self.dec_nn(z)
        return out

    def forward(self, x):
        z = self.encode(x)
        return self.decode(z)


class Conv_AE(nn.Module):
    def __init__(self, n_features, z_dim, *args, **kwargs):
        super(Conv_AE, self).__init__(*args, **kwargs)

        self.q_z_mid_dim = 2000
        self.q_z_output_dim = 72128

        # Encoder

        # Conv Layers
        self.q_z_conv = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=(2, 5), stride=(1), padding=(1)),
            # nn.BatchNorm2d(8),
            nn.ReLU(),
            nn.Conv2d(8, 16, kernel_size=(3), stride=(1), padding=(1)),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=(3), stride=(1), padding=(0)),
            # nn.BatchNorm2d(32),
            nn.ReLU(),
        )
        # Flatten
        self.flatten = nn.Flatten(start_dim=1)
        # Linear layers
        self.q_z_lin = nn.Sequential(
            nn.Linear(self.q_z_output_dim, self.q_z_mid_dim),
            nn.ReLU(),
            # nn.BatchNorm1d(self.q_z_output_dim),
            nn.Linear(self.q_z_mid_dim, z_dim),
            nn.ReLU(),
        )

        # Decoder

        # Linear layers
        self.p_x_lin = nn.Sequential(
            nn.Linear(z_dim, self.q_z_mid_dim),
            nn.ReLU(),
            # nn.BatchNorm1d(self.q_z_output_dim),
            nn.Linear(self.q_z_mid_dim, self.q_z_output_dim),
            nn.ReLU()
            # nn.BatchNorm1d(42720)
        )
        # Conv Layers
        self.p_x_conv = nn.Sequential(
            nn.ConvTranspose2d(32, 16, kernel_size=(3), stride=(1), padding=(0)),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 8, kernel_size=(3), stride=(1), padding=(1)),
            nn.BatchNorm2d(8),
            nn.ReLU(),
            nn.ConvTranspose2d(8, 1, kernel_size=(2, 5), stride=(1), padding=(1)),
        )

    def encode(self, x):
        # Conv
        out = self.q_z_conv(x)
        # Flatten
        out = self.flatten(out)
        # Dense
        out = self.q_z_lin(out)
        return out

    def decode(self, z):
        # Dense
        out = self.p_x_lin(z)
        # Unflatten
        out = out.view(out.size(0), 32, 49, 46)
        # Conv transpose
        out = self.p_x_conv(out)
        return out

    def forward(self, x):
        z = self.encode(x)
        out = self.decode(z)
        return out
