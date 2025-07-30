import os
from tqdm import tqdm
import pandas as pd
import argschema as ags
from morph_utils.ccf import projection_matrix_for_swc

class IO_Schema(ags.ArgSchema):
    input_swc_file = ags.fields.InputFile(description='directory with micron resolution ccf registered files')
    output_projection_csv = ags.fields.OutputFile(description="output projection csv")
    mask_method = ags.fields.Str(description = " 'tip_and_branch', 'branch', 'tip', or 'tip_or_branch' ")
    apply_mask_at_cortical_parent_level = ags.fields.Bool( descriptions='If True, the `mask_method` will be applied at aggregated cortical regions')

    projection_threshold = ags.fields.Int(default=0)
    normalize_proj_mat = ags.fields.Boolean(default=True)
    count_method = ags.fields.String(default="node", description="should be a member of ['node','tip','branch']")
    annotation_path = ags.fields.Str(default="",description = "Optional. Path to annotation .nrrd file. Defaults to 10um ccf atlas")
    resolution = ags.fields.Int(default=10, description="Optional. ccf resolution (micron/pixel")
    volume_shape = ags.fields.List(ags.fields.Int, default=[1320, 800, 1140], description = "Optional. Size of input annotation")
    resample_spacing = ags.fields.Float(allow_none=True, default=None, description = 'internode spacing to resample input morphology with')

def normalize_projection_columns_per_cell(input_df, projection_column_identifiers=['ipsi', 'contra']):
    """
    :param input_df:  input projection df
    :param projection_column_identifiers: list of identifiers for projection columns. i.e. strings that identify projection columns from metadata columns
    :return: normalized projection matrix
    """
    proj_cols = [c for c in input_df.columns if any([ider in c for ider in projection_column_identifiers])]
    input_df[proj_cols] = input_df[proj_cols].fillna(0)

    res = input_df[proj_cols].T / input_df[proj_cols].sum(axis=1)
    input_df[proj_cols] = res.T

    return input_df


def main(input_swc_file, 
         output_projection_csv, 
         resolution, 
         projection_threshold, 
         normalize_proj_mat,
         mask_method,
         count_method,
         annotation_path,
         volume_shape,
         resample_spacing,
         apply_mask_at_cortical_parent_level,
         **kwargs):
    
    if annotation_path == "":
        annotation_path = None
    
    if mask_method is None:
        mask_method = "None"
    if mask_method not in [None, 'None', 'tip_and_branch', 'branch', 'tip', 'tip_or_branch']:
        raise ValueError(f"Invalid mask_method provided {mask_method}")  
    
    results = []
    res = projection_matrix_for_swc(input_swc_file=input_swc_file, 
                                    count_method = count_method, 
                                    mask_method = mask_method,
                                    annotation=None, 
                                    annotation_path = annotation_path, 
                                    volume_shape=volume_shape,
                                    resolution=resolution,
                                    resample_spacing=resample_spacing,
                                    apply_mask_at_cortical_parent_level=apply_mask_at_cortical_parent_level)
    results = [res]
        
    output_projection_csv = output_projection_csv.replace(".csv", f"_{mask_method}.csv")
    projection_records = {}
    # branch_and_tip_projection_records = {}
    for res in results:
        fn = os.path.abspath(res[0])
        proj_records = res[1]
        # brnch_tip_records = res[1]

        projection_records[fn] = proj_records
        # branch_and_tip_projection_records[fn] = brnch_tip_records

    proj_df = pd.DataFrame(projection_records).T.fillna(0)
    # proj_df_mask = pd.DataFrame(branch_and_tip_projection_records).T.fillna(0)

    proj_df.to_csv(output_projection_csv)
    # proj_df_mask.to_csv(output_projection_csv_tip_branch_mask)
    print(proj_df.head())
    if projection_threshold != 0:
        output_projection_csv = output_projection_csv.replace(".csv",
                                                              "{}thresh.csv".format(projection_threshold))
        # output_projection_csv_tip_branch_mask = output_projection_csv_tip_branch_mask.replace(".csv",
        #                                                                                       "{}thresh.csv".format(
        #                                                                                           projection_threshold))

        proj_df_arr = proj_df.values
        proj_df_arr[proj_df_arr < projection_threshold] = 0
        proj_df = pd.DataFrame(proj_df_arr, columns=proj_df.columns, index=proj_df.index)
        proj_df.to_csv(output_projection_csv)

        # proj_df_mask_arr = proj_df_mask.values
        # proj_df_mask_arr[proj_df_mask_arr < projection_threshold] = 0
        # proj_df_mask = pd.DataFrame(proj_df_mask_arr, columns=proj_df_mask.columns, index=proj_df_mask.index)
        # proj_df_mask.to_csv(output_projection_csv_tip_branch_mask)

    if normalize_proj_mat:
        output_projection_csv = output_projection_csv.replace(".csv", "_norm.csv")
        # output_projection_csv_tip_branch_mask = output_projection_csv_tip_branch_mask.replace(".csv", "_norm.csv")

        proj_df = normalize_projection_columns_per_cell(proj_df)
        proj_df.to_csv(output_projection_csv)

        # proj_df_mask = normalize_projection_columns_per_cell(proj_df_mask)
        # proj_df_mask.to_csv(output_projection_csv_tip_branch_mask)

def console_script():
    module = ags.ArgSchemaParser(schema_type=IO_Schema)
    main(**module.args)

if __name__ == "__main__":
    module = ags.ArgSchemaParser(schema_type=IO_Schema)
    main(**module.args)
