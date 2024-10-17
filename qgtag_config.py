
# === Configuration options ===

def set_config(c):
    c.input_path = '/users/dshutong/.energyflow/datasets/sorted_QG_jets_17.npz'
    #c.input_path                   = "/users/dshutong/.energyflow/datasets/top_qcd_0.npz"
    #c.input_path                   = "data/qgtag/QG_jets.npz"
    c.data_dimension               = 2
    c.compression_ratio            = 15
    c.apply_normalization          = False
    c.model_name                   = "AE"
    c.epochs                       = 1000
    c.lr                           = 0.001
    c.batch_size                   = 512 # was 512
    c.early_stopping               = True
    c.lr_scheduler                 = True




# === Additional configuration options ===

    c.early_stopping_patience      = 100
    c.min_delta                    = 0
    c.lr_scheduler_patience        = 100
    c.custom_norm                  = False
    c.l1                           = True
    c.reg_param                    = 0.001
    c.RHO                          = 0.05
    c.test_size                    = 0.15 # was 0
    # c.number_of_columns            = 24
    # c.latent_space_size            = 12
    c.extra_compression            = False
    c.intermittent_model_saving    = False
    c.intermittent_saving_patience = 100
    c.activation_extraction        = False
