import mdtraj as md
import argparse
import numpy as np
import os

class MD_initializer():
	
	def __init__(self):	
		self.save_folder = ''
		self.file_name_end = ''
		self.sub_units = []
		return

	
	def initialize_trajectory(self, parser):
		parser = self.setParserArguments(parser)
		args = parser.parse_args()
		
		# Get command line input parameters
		self.save_folder = args.out_directory
		self.file_name_end = args.file_end_name
		
		# Set output directory  
		#Put / at end of out directory if not present. Check so that folder extsts, otherwise construct it.
		if self.save_folder !='':
			if self.save_folder[-1] != '/': self.save_folder += '/'; args.out_directory = self.save_folder
			if not os.path.exists(self.save_folder):
				os.makedirs(self.save_folder)
		print('Saving output files in directory: ' + self.save_folder)
	
		# Get trajectories	
		if args.multiple_trajectories: #load multiple trajectories and keep them separate
			traj = self.getMultipleTrajectories(args.topology_file, args.trajectory_files, args.trajectory_file_directory, float(args.dt))
		elif args.downsample_and_save:
			self.downsampleTrajectories(args.topology_file, args.trajectory_files, float(args.dt))
			return [],[]
		else:
			traj = self.getTrajectory(args.topology_file[0], args.trajectory_files, float(args.dt))	
		print('File end name: ' + self.file_name_end)
		return traj, args


	def setParserArguments(self,parser):
		parser.add_argument('-top','--topology_file',help='Input 1 topology file (.gro, .pdb, etc)',type=str,default='',nargs='+')
		parser.add_argument('-trj','--trajectory_files',help='Input trajectory files (.xtc, .dcd, etc)',nargs='+',default='')

		parser.add_argument('-trjdir','--trajectory_file_directory',help='Input directory with trajectories (.xtc, .dcd, etc.); load all trajectories in the specified directory.',default='')	
		parser.add_argument('-multitraj','--multiple_trajectories',help='Flag for reading multiple trajectories. Need as many arguments in -top as in -trj',action='store_true')
		parser.add_argument('-dt','--dt',help='Keep every dt frame.',default=1)
		parser.add_argument('-downsample','--downsample_and_save',help='Downsample and save downsampled trajectories. The trajectories will be treated as continuum but saved as separate parts.',action='store_true')

		parser.add_argument('-fe','--file_end_name',type=str,help='Output file end name (optional)', default='')
		parser.add_argument('-od','--out_directory',type=str,help='The directory where data should be saved (optional)',default='')

		return parser


	def getTrajectory(self, topology_file, trajectory_files, dt):
		# Print file names in a string 
		trajectoryString = "Trajectory files: "
		topologyString = "Topology files: " + topology_file
		for i in range(0,len(trajectory_files)):trajectoryString += trajectory_files[i] + " "
		print(topologyString)
		print(trajectoryString)
		
		# Joining trajectories
		traj = md.load(trajectory_files[0], top = topology_file, stride=int(dt))
		for i in range(1,len(trajectory_files)):
			print("Joining trajectory: " + str(i) + 'with stride =' + str(int(dt)))
			trajectory = md.load(trajectory_files[i], top = topology_file, stride=int(dt))
			traj = traj.join(trajectory)
			print("Number of frames: " + str(traj.n_frames))

		return traj
	

	def getMultipleTrajectories(self, topology_files, trajectory_files, trajectory_file_directory, dt):
		# Load multiple trajectories and keep them separate in a list
		trajs = []
		do_separate_topologies = (len(topology_files)>1)
		
		if trajectory_file_directory == '':
			# Loop over pre-specified trajectories
			for i in range(len(trajectory_files)):
				if do_separate_topologies:
					trajs.append(self.getTrajectory(topology_files[i], [trajectory_files[i]], dt))
				else:
					trajs.append(self.getTrajectory(topology_files[0], [trajectory_files[i]], dt))
		else:
			# Loop over all trajectory files within the specified directory
			counter = 0
			for trajectory_file in os.listdir(trajectory_file_directory):
				if trajectory_file.endswith(".dcd") or trajectory_file.endswith(".xtc"): 
					trajs.append(self.getTrajectory(topology_files[0], [trajectory_file_directory+trajectory_file], dt))
		
		return trajs

	def downsampleTrajectories(self, topology_file, trajectory_files, dt):
		# Read and slice trajectory to reduce trajectory size. The downsampled trajectories are saved in self.saveFolder.
		trajectoryString = "Trajectory files: "
		topologyString = "Topology files: " + topology_file
		
		# Print file names in string
		for i in range(0,len(trajectory_files)):trajectoryString += trajectory_files[i] + " "
		print(trajectoryString)
		print(topologyString)
		
		# Slice and save trajectories
		trajectory = md.load(trajectory_files[0], top = topology_file, stride=int(dt))
		tajectory.save_xtc(self.save_folder + self.file_name_end + str(0)+ '.xtc')
		for i in range(1,len(trajectory_files)):
			print("Slicing and saving trajectory: " + str(i+1))
			trajectory = md.load(trajectory_files[i], top = topology_file, stride=int(dt))
			trajectory.save_xtc(self.save_folder + self.file_name_end + str(i) + '.xtc')

	def getSubUnits(self):
		return self.sub_units

	def getFileEndName(self):
		return self.file_name_end

	def getSaveFolder(self):
		return self.save_folder


