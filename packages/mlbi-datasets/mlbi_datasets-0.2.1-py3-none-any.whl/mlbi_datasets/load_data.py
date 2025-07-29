import gdown, gzip, shutil, os, tarfile
import anndata 

def download_from_google_drive( file_id, out_path = 'downloaded' ):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    gdown.download(url, out_path, quiet = False)
    return out_path

def decompress_gz( file_in, file_out, remove_gz = True ):
    try:
        with gzip.open(file_in, 'rb') as f_in:
            with open(file_out, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                if remove_gz:
                    os.remove(file_in)
                print(f'File saved to: {file_out}')
                return file_out
    except:
        return None

def decompress_tar_gz( file_in, remove_org = True ):

    try:
        extract_path = 'extract_tmp'
        if os.path.isdir(extract_path):
            shutil.rmtree(extract_path)
    
        with tarfile.open(file_in, "r:gz") as tar:
            tar.extractall(path=extract_path)
    
        file_h5ad = os.listdir(extract_path)[0]
        file = extract_path + '/%s' % file_h5ad
        if os.path.isdir(file):
            file_h5ad = os.listdir(file)[0]
            file = file + '/%s' % (file_h5ad)
    
        if os.path.isfile(file_h5ad):
            os.remove(file_h5ad)
    
        if not os.path.isfile(file_h5ad):
           shutil.move(file, '.')
    
        shutil.rmtree(extract_path)
        if remove_org:
            os.remove(file_in)
    
        print(f'File saved to: {file_h5ad}')
        return file_h5ad
    except:
        return None


def load_h5ad( tissue, file_type = 'gz' ):

    tlst = ['Melanoma', 'NSCLC', 'CRC', 'BRCA', 'PDAC', 'Colitis-mm', 'Colitis-mm-full', 'Colitis-hs' ]
    
    if tissue in ['Lung', 'NSCLC']:
        file_id = '1yMM4eXAdhRDJdyloHACP46TNCpVFnjqD'       
        ## Lung Cancer dataset: selected from GSE131907
    elif tissue in ['Intestine', 'Colon', 'CRC']:
        tissue = 'Intestine'
        file_id = '1oz1USuvIT7VNSmS2WhJuHDZQhkCH6IPY'  
        ## Colorectal Cancer dataset: selected from GSE132465
    elif tissue in ['Breast', 'BRCA']:
        file_id = '158LUiHiJNFzYvqY-QzMUm5cvIznBrUAV'     
        ## Breast Cancer dataset: selected from GSE161529
    elif tissue in ['Pancreas', 'PDAC']:
        file_id = '1OgTsyXczHQoV6PJyo_rfNBDJRRHXRhb-'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    elif tissue == 'Colitis-mm':
        file_id = '11cVrrxaeai87pKKiUcSjCd-Lw7hkrzrI'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    elif tissue == 'Colitis-mm-full':
        file_id = '1klU5SVZ8VmBpIhUPmDkFr_1TycqCdHk_'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    elif tissue == 'Colitis-hs':
        file_id = '12641IgY-cidvomm4ZZziAcTplYngaq0C'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    elif tissue == 'Melanoma':
        file_id = '1hlGXEi9UEIZiHGHZJgxZPClVsPdHpvZS'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    else:
        print('tissue must be one of %s. ' % ', '.join(tlst))
        return None

    file_h5ad = None
    file_down = download_from_google_drive( file_id )
    # file_h5ad = decompress_gz( file_down, '%s.h5ad' % tissue, remove_gz = True )
    if file_type == 'tar.gz':
        file_h5ad = decompress_tar_gz( file_down, remove_org = True )    
        adata = anndata.read_h5ad(file_h5ad)
    elif file_type == 'gz':
        file_h5ad = decompress_gz( file_down, '%s.h5ad' % tissue, remove_gz = True )
        adata = anndata.read_h5ad(file_h5ad)

    return file_h5ad


def load_anndata( tissue ):

    file_h5ad = load_h5ad( tissue )
    if file_h5ad is None:
        return None
    else:
        adata = anndata.read_h5ad(file_h5ad)
        return adata


def load_sample_data( file_id_or_tissue_name, file_type = 'tar.gz' ):

    tlst = ['Melanoma', 'NSCLC', 'CRC', 'BRCA', 'PDAC', 'Colitis-mm', 'Colitis-mm-full', 'Colitis-hs' ] 
    tlst = tlst + ['Lung', 'Breast', 'Pancreas', 'Colon', 'Intestine']
    
    if file_id_or_tissue_name in tlst:
        return load_anndata( file_id_or_tissue_name )
    else:
        adata = None
        try:
            file_down = download_from_google_drive( file_id_or_tissue_name )
        except:
            print('ERROR: The file_id you requested does not exist.')
            print('You can try one of %s. ' % ', '.join(tlst))
            return None

        file_h5ad = None
        if file_type == 'tar.gz':
            file_h5ad = decompress_tar_gz( file_down, remove_org = True )   
                
        elif file_type == 'gz':
            file_h5ad = decompress_gz( file_down, 'downloaded.h5ad', remove_gz = True )

        if file_h5ad is None:
            print('ERROR: The file_type might be a wrong one.')
            print('You can try with one of tar.gz or gz for file_type argument. ')
            print('Or, You can try one of %s for file_id_or_tissue_name. ' % ', '.join(tlst))
            return None
        else:
            try:
                adata = anndata.read_h5ad(file_h5ad)
            except:
                print('ERROR: Cannot read the downloaded file.')
                print('You can try one of %s for file_id_or_tissue_name. ' % ', '.join(tlst))
                return None
                
        return adata

'''
file_id = '1Xazyv4JhWlhYkDVk51KXaL3DDlAoxftp' ## GSE131907: NSCLC 
file_id = '1XbX8Q3dH1kOWnM6ppms4BR2ukEAKYisB' ## GSE161529: BRCA 
file_id = '1XbYJQpyo8PaoL_vpjBt4YI5tTi8pgV5o' ## GSE155698: PDAC 
file_id = '1Xb_dzJDgt_RlkXk5nP0jgRUz_aFdP0G9' ## GSE132465: Colon 
'''
def load_scoda_processed_anndata( tissue = None, file_type = 'tar.gz' ):

    tlst = ['NSCLC', 'CRC', 'BRCA', 'PDAC', 'Colitis-mm', 'Colitis-mm-full', 'Colitis-hs' ]
    if (tissue in ['Lung', 'NSCLC']):
        file_id = '1Xazyv4JhWlhYkDVk51KXaL3DDlAoxftp'       
        ## Lung Cancer dataset: selected from GSE131907
    elif (tissue in ['Intestine', 'Colon', 'CRC']):
        tissue = 'Intestine'
        file_id = '1Xb_dzJDgt_RlkXk5nP0jgRUz_aFdP0G9'  
        ## Colorectal Cancer dataset: selected from GSE132465
    elif (tissue in ['Breast', 'BRCA']):
        file_id = '1XbX8Q3dH1kOWnM6ppms4BR2ukEAKYisB'     
        ## Breast Cancer dataset: selected from GSE161529
    elif (tissue in ['Pancreas', 'PDAC']):
        file_id = '1XbYJQpyo8PaoL_vpjBt4YI5tTi8pgV5o'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    elif tissue == 'Colitis-mm':
        file_id = '1QgdmySeTYQjW0NfNxbpaokU22VpEpcHA'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    elif tissue == 'Colitis-mm-full':
        file_id = '1K7p0mFVRv9BIDkWZR41iWX2LzFcljWzg'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    elif tissue == 'Colitis-hs':
        file_id = '1qRjo2iPlDVxF88umvpxiNGXk6jFK9dbb'     
        ## Pancreatic Cancer (PDAC) dataset: selected from GSE161529
    else:
        print('tissue must be one of %s. ' % ', '.join(tlst))
        return None

    file_h5ad = None
    try:
        file_down = download_from_google_drive( file_id )
        if file_type == 'tar.gz':
            file_h5ad = decompress_tar_gz( file_down, remove_org = True )
        elif file_type == 'gz':
            file_h5ad = decompress_gz( file_down, '%s.h5ad' % tissue, remove_gz = True )
    except:
        pass

    if file_h5ad is None:
        return None
    else:
        adata = anndata.read_h5ad(file_h5ad)
        return adata


def load_scoda_processed_sample_data( file_id_or_tissue_name = None, file_type = 'tar.gz' ):

    file_type = 'tar.gz'
    tlst = ['NSCLC', 'CRC', 'BRCA', 'PDAC', 'Colitis-mm', 'Colitis-mm-full', 'Colitis-hs' ] 
    tlst = tlst + ['Lung', 'Breast', 'Pancreas', 'Colon', 'Intestine']

    if file_id_or_tissue_name in tlst:
        return load_scoda_processed_anndata( file_id_or_tissue_name, file_type )
    else:
        adata = None
        try:
            file_down = download_from_google_drive( file_id_or_tissue_name )
        except:
            print('ERROR: The file_id you requested does not exist.')
            print('You can try one of %s. ' % ', '.join(tlst))
            return None

        if file_type == 'tar.gz':
            file_h5ad = decompress_tar_gz( file_down, remove_org = True )    
            adata = anndata.read_h5ad(file_h5ad)
        elif file_type == 'gz':
            file_h5ad = decompress_gz( file_down, 'downloaded.h5ad', remove_gz = True )
            adata = anndata.read_h5ad(file_h5ad)

        print('ERROR: The file_type might be a wrong one.')
        print('You can try with one of tar.gz or gz for file_type argument. ')
        print('Or, You can try one of %s for file_id_or_tissue_name. ' % ', '.join(tlst))
        return None
            
        return adata

