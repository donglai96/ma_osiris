import os 
import numpy as np
import string
import h5py
import matplotlib.pyplot as plt
from ..readh5.readh5 import convert_h5_to_data


class diag1D:
    def __init__(self, data_dir = None, input_file = None):
        """This is a class for osiris diagnostic data

        Args:
            data_dir (str, optional): The directory of the data. Defaults to None.
            data_name (str, optional): The name of the data. Defaults to None.
        """
        self.data_dir = data_dir
        self.input_file = input_file
        
    def get_parameters(self):
        """
        Get the parameters before diag begins
        """
        self.parameters = {}
        with open(self.input_file) as f:
            for line in f:
                #print(line)
                if ('reports' in line) or ('diag' in line) or('phasespace' in line):
                    continue
                if '!' in line:
                    # ignore the comments
                    line = line[:line.find('!')]
                
                if line.count('=')>=2:
                    # seperate by comma
                    equation_list = line.split(",")
                    # only select the equation with '='
                    equation_list = [s for s in equation_list  if "=" in s]
                elif '=' in line:
                    if ('(' in line) and  (')' in line) and (':' in line):
                        equation_list = [line[:-2]]# remove ',\n'
                    else:
                        equation_list = line.rsplit(",")[:-1]
                else:
                    equation_list = None 
                    continue
                #print(equation_list)
                for equation in equation_list:
                    (key, val) = equation.split("=")
                    key = key.translate({ord(c): None for c in string.whitespace})[
                        :]
                    val_clean = val.translate({ord(c): None for c in string.whitespace})[
                        :]
                if ('"' in val_clean) or ("'" in val_clean):
                        # remove quotation marks
                    self.parameters[key] = val_clean[1:-1]
                
                    
                elif '.true' in val_clean:
                    self.parameters[key] = 'True'
                elif '.false' in val_clean:
                    self.parameters[key] = 'False'
                elif 'd0' or '.' in val_clean:
                    #print(val_clean)
                    string_array = np.array(val_clean.replace("d","e").split(","))
                    self.parameters[key] = string_array.astype(float)  # change to float
                    
                else:
                    self.parameters[key] = int(val_clean)  # change to int
        print("Get parameters done")
        print(self.parameters)
    
    def phasespace(self, dataset = 'p1x1', species = 'electrons',time = 0, xlim = [-1, -1], ylim = [-1, -1], return_data = False):
        """
        Get the phase space of the 1D simulation

        Args:
            dataset (str, optional): _description_. Defaults to 'p1x1'.
            species (str, optional): _description_. Defaults to 'electrons'.
            time (int, optional): _description_. Defaults to 0.
            xlim (list, optiondiag_testal): _description_. Defaults to [-1, -1].
        """
        phase_dir = os.path.join(self.data_dir, 'MS', 'PHA', dataset, species)
        files = sorted(os.listdir(phase_dir))
        
        i = 0
        for j in range(len(files)):
            fhere = h5py.File(os.path.join(phase_dir,files[j]), 'r')
            #print(list(fhere.attrs))
            if(fhere.attrs['TIME'] >= time):
                i = j
                file_path = os.path.join(phase_dir,files[j])
                break
            
        if return_data:
            
                
            print(file_path)       
            #fhere = h5py.File(os.path.join(field_dir,files[i]), 'r')
            field_info = convert_h5_to_data(file_path)
            return field_info, fhere.attrs['TIME']
            

        fhere = h5py.File(os.path.join(phase_dir,files[i]), 'r')

        plt.figure(figsize=(6, 3.2))
        plt.title(dataset+' phasespace at t = '+str(fhere.attrs['TIME']))
        plt.xlabel('$x_1 [c/\omega_p]$')
        if(len(fhere['AXIS']) == 1):
            plt.ylabel('$n [n_0]$')
        if(len(fhere['AXIS']) == 2):
            plt.ylabel('$p_1 [m_ec]$')

        if(len(fhere['AXIS']) == 1):

            xaxismin = fhere['AXIS']['AXIS1'][0]
            xaxismax = fhere['AXIS']['AXIS1'][1]

            nx = len(fhere[dataset][:])
            dx = (xaxismax-xaxismin)/nx
            # print(dx)
            # print(nx)
            # print(xaxismax)
            # print(xaxismin)

            plt.plot(np.abs(fhere[dataset][:]))
            plt.show()
            

        elif(len(fhere['AXIS']) == 2):

            xaxismin = fhere['AXIS']['AXIS1'][0]
            xaxismax = fhere['AXIS']['AXIS1'][1]
            yaxismin = fhere['AXIS']['AXIS2'][0]
            yaxismax = fhere['AXIS']['AXIS2'][1]

            plt.imshow(np.log(np.abs(fhere[dataset][:,:]+1e-12)),
                    aspect='auto',
                    extent=[xaxismin, xaxismax, yaxismin, yaxismax])
            plt.colorbar(orientation='vertical')

        if return_data:
            return fhere[dataset][:,:]
        if(xlim != [-1,-1]):
            plt.xlim(xlim)
        
        if(ylim != [-1,-1]):
            plt.ylim(ylim)
        # if(zlim != [-1,-1]):
        #     plt.clim(zlim)

        plt.show()
        return fhere
    
    def field(self, dataset='e3',xlim=[-1,-1],plotdata=[],species='electrons', time = 0):

        field_dir  = os.path.join(self.data_dir, 'MS', 'FLD', dataset)
        files = sorted(os.listdir(field_dir))
        n_files = len(files)
        file_0 = os.path.join(field_dir,files[0])
        print(file_0)
        field_0_info = convert_h5_to_data(file_0)
        
        
        self.field_name = dataset
        self.field_dt = field_0_info['SIMULATION']['attributes']['DT'][0]
        field_xlim = field_0_info['AXIS/AXIS1']['data']
        self.field_x = np.linspace(field_xlim[0], field_xlim[1], len(field_0_info[dataset]['data']))
        self.field_t = np.arange(0, n_files)*self.field_dt
        
        self.field_data = np.zeros((n_files, len(self.field_x)))
        for i in range(n_files):
            file = os.path.join(field_dir,files[i])
            field_info = convert_h5_to_data(file)
            self.field_data[i,:] = field_info[dataset]['data']
            
            
    def get_field_data(self, dataset = 'e1', time = 0):
        field_dir = os.path.join(self.data_dir, 'MS', 'FLD', dataset)
        files = sorted(os.listdir(field_dir))
        
        i = 0
        for j in range(len(files)):
            fhere = h5py.File(os.path.join(field_dir,files[j]), 'r')
            #print(list(fhere.attrs))
            if(fhere.attrs['TIME'] >= time):
                i = j
                file_path = os.path.join(field_dir,files[j])
                break
        print(file_path)       
        #fhere = h5py.File(os.path.join(field_dir,files[i]), 'r')
        field_info = convert_h5_to_data(file_path)
        return field_info, fhere.attrs['TIME']
        
        
    