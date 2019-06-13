# This script overlays side chain fragments from an xyz file onto residues from a pdb file. The xyz and pdb file must belong to the same frame of the trajectory, because this script directly compares Cartesian coordinates of atoms on the two files, and detects if any atom/residue is missing. 
# to run this script, type this into the terminal: awk -f Detect_missing_residue_from_SolEFP_calculations.awk input-file.pdb SolEFP-output-file.xyz 

BEGIN{
	ORI_NR=52905; #total number of lines in original pdb file
	SOL_NR=6333; #total number of lines in solefp debug file 
	TOT_NR=ORI_NR+SOL_NR;
	ori_count=1;
	sol_count=1;
	RES_NUM=148; #total number of residues in original pdb file 
}

	

	function f1(x){
		split(x,a,".");
		return a[1]"."substr(a[2],1,1)
	}

{
	if (NR<=ORI_NR && $4!="HOH" && $4!="CL" && $4!="NA" ){
		oriresnum[ori_count]=$6;
		oriresname[$6,ori_count]=$4;  
	       	orix[ori_count]=int($7); 
		oriy[ori_count]=int($8);
		oriz[ori_count]=int($9);
		oriatmname[ori_count]=$NF;
		ori_count+=1;
	}

	if (NR>ORI_NR && NF>=3){
		solx[sol_count]=int($2); 
		soly[sol_count]=int($3);
		solz[sol_count]=int($4);
		solatmname[sol_count]=$1;
		sol_count+=1;
	}

}
END{

	print ("Comparing Cartesian coordinates of atoms (accurate to integer level) ...")
	for (i=1; i<sol_count;i++){
	# check atom by atom 		
		j=1;
		match_found=0;
		# check if atom in original list is also in the solefp list 
		while (j<ori_count && match_found==0){
			if (solx[i]==orix[j] && soly[i]==oriy[j] && solz[i]==oriz[j] && solatmname[i]==oriatmname[j]){
				match_found=1;
			}
			else{
				j+=1
			}
		}
		# record matched atom
		if (match_found==1){
			if (hasatm[oriresnum[j]]!=0){ 
				hasatm[oriresnum[j]]=hasatm[oriresnum[j]]" "oriatmname[j]
			}
			else{
				hasatm[oriresnum[j]]=oriresname[oriresnum[j],j]" "oriresnum[j]" contains "oriatmname[j]
		        }
		}
	}




	for (res=1; res<=RES_NUM; res++){
		if (int(res in hasatm)!=int(0)){
			print hasatm[res];
		}
		else{
			print "missing residue "res;
		}
	}	

}


