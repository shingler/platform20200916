#!/usr/bin/python
# -*- coding:utf-8 -*-
# 从数据库读取各种配置
from sqlalchemy import and_

from src import db
from src.models import dms


class Setup:
    # 读取api_setup
    @staticmethod
    def load_api_setup(company_code, api_code) -> dms.ApiSetup:
        api_setup = db.session.query(dms.ApiSetup).filter(dms.ApiSetup.Company_Code == company_code) \
            .filter(dms.ApiSetup.API_Code == api_code).first()
        return api_setup

    # 读取api_p_in
    @staticmethod
    def load_api_p_in(company_code, api_code) -> list:
        p_in_list = db.session.query(dms.ApiPInSetup).filter(
            and_(dms.ApiPInSetup.Company_Code == company_code, dms.ApiPInSetup.API_Code == api_code)).all()
        return p_in_list

    # 读取出参配置配置
    @staticmethod
    def load_api_p_out_nodes(company_code, api_code, node_type="General", depth=2) -> dict:
        node_dict = {}
        api_p_out_config = db.session.query(dms.ApiPOutSetup) \
            .filter(dms.ApiPOutSetup.Company_Code == company_code) \
            .filter(dms.ApiPOutSetup.API_Code == api_code) \
            .filter(dms.ApiPOutSetup.Level == depth) \
            .filter(dms.ApiPOutSetup.Parent_Node_Name == node_type) \
            .order_by(dms.ApiPOutSetup.Sequence.asc()).all()
        for one in api_p_out_config:
            if one.P_Name not in node_dict:
                node_dict[one.P_Name] = one
        # print(node_dict)
        return node_dict

    # 按层级关系读取所有出参配置
    @staticmethod
    def load_api_p_out(company_code, api_code) -> dict:
        node_dict = {}
        api_p_out_config = db.session.query(dms.ApiPOutSetup) \
            .filter(dms.ApiPOutSetup.Company_Code == company_code) \
            .filter(dms.ApiPOutSetup.API_Code == api_code) \
            .order_by(dms.ApiPOutSetup.Sequence.asc()).all()
        for one in api_p_out_config:
            # 根节点
            if one.Parent_Node_Name == '':
                one.Parent_Node_Name = "/"
            # 构造上级节点
            if one.Parent_Node_Name not in node_dict:
                node_dict[one.Parent_Node_Name] = {}

            # 按层级组装
            node_dict[one.Parent_Node_Name][one.P_Name] = one

        # print(node_dict)
        return node_dict
