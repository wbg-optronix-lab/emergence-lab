# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from core.models import Process, ProcessNode


class ProcessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Process
        fields = ('uuid_full', 'uuid', 'created', 'modified', 'comment',
                  'is_destructive')


class ProcessRootNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessNode
        fields = ('uuid_full', 'uuid', 'created', 'modified', 'comment',
                  'children')


class ProcessParentNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessNode
        fields = ('uuid_full', 'uuid', 'created', 'modified', 'comment',
                  'parent', 'process', 'piece')


class ProcessNodeSerializer(serializers.ModelSerializer):
    process = ProcessSerializer()
    parent = ProcessParentNodeSerializer()

    class Meta:
        model = ProcessNode
        fields = ('uuid_full', 'uuid', 'created', 'modified', 'comment',
                  'parent', 'children', 'process', 'piece')
        depth = 1
